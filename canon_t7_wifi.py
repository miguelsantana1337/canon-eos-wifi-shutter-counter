#!/usr/bin/env python3
"""Experimental Canon EOS shutter counter reader via Wi-Fi PTP/IP and PCAP.

Live Wi-Fi mode has NOT been validated end-to-end on camera hardware.
Python 3.9+ standard library only.
"""
import argparse
import json
import socket
import struct
import sys
import time
import uuid
from pathlib import Path

PTPIP_PORT = 15740
EOS_SHUTTER_COUNTER = 0xD1AC
EOS_PROPERTY_CHANGED = 0xC189
PTP_SUCCESS = 0x2001
MAX_FRAME_SIZE = 32 * 1024 * 1024


class PTPError(Exception):
    """Invalid camera response or malformed capture."""


def find_shutter_counter(events):
    """Extract property 0xD1AC from Canon EOS property-changed events."""
    pos = 0
    while pos + 8 <= len(events):
        size, event = struct.unpack_from('<II', events, pos)
        if size < 8 or pos + size > len(events):
            break
        if event == EOS_PROPERTY_CHANGED and size >= 16:
            prop, value = struct.unpack_from('<II', events, pos + 8)
            if prop == EOS_SHUTTER_COUNTER:
                return value
        pos += size
    return None


def recv_exact(sock, size):
    data = bytearray()
    while len(data) < size:
        part = sock.recv(size - len(data))
        if not part:
            raise PTPError('Camera disconnected.')
        data.extend(part)
    return bytes(data)


def recv_frame(sock):
    length, kind = struct.unpack('<II', recv_exact(sock, 8))
    if not 8 <= length <= MAX_FRAME_SIZE:
        raise PTPError('Invalid PTP/IP frame size.')
    return kind, recv_exact(sock, length - 8)


def send_frame(sock, kind, payload=b''):
    sock.sendall(struct.pack('<II', len(payload) + 8, kind) + payload)


def connect_camera(ip, timeout):
    command = socket.create_connection((ip, PTPIP_PORT), timeout=timeout)
    command.settimeout(timeout)
    try:
        name = 'CanonEOSOpenReader'.encode('utf-16le') + b'\x00\x00'
        send_frame(command, 1, uuid.uuid4().bytes + name + struct.pack('<I', 0x10000))
        kind, ack = recv_frame(command)
        if kind != 2 or len(ack) < 4:
            raise PTPError('Camera declined command connection.')
        connection_id = struct.unpack_from('<I', ack)[0]
        event = socket.create_connection((ip, PTPIP_PORT), timeout=timeout)
        event.settimeout(timeout)
        try:
            send_frame(event, 3, struct.pack('<I', connection_id))
            kind, _ = recv_frame(event)
            if kind != 4:
                raise PTPError('Camera declined event connection.')
        except Exception:
            event.close()
            raise
        return command, event
    except Exception:
        command.close()
        raise


def operation(sock, opcode, transaction, params=()):
    payload = struct.pack('<IHI', 1, opcode, transaction)
    payload += b''.join(struct.pack('<I', x) for x in params)
    send_frame(sock, 6, payload)
    chunks = []
    while True:
        kind, body = recv_frame(sock)
        if kind == 9:
            continue
        if kind in (10, 12):
            if len(body) < 4 or struct.unpack_from('<I', body)[0] != transaction:
                raise PTPError('Invalid data transaction.')
            chunks.append(body[4:])
        elif kind == 7:
            if len(body) < 6:
                raise PTPError('Invalid operation response.')
            result, received = struct.unpack_from('<HI', body)
            if received != transaction:
                raise PTPError('Unexpected transaction.')
            return result, b''.join(chunks)
        elif kind != 8:
            raise PTPError('Unexpected PTP/IP packet type.')


def read_live(ip='192.168.1.2', timeout=8):
    """Experimental: camera must be paired and remote control enabled."""
    command, event = connect_camera(ip, timeout)
    try:
        steps = ((0x1002, 0, (1,)), (0x1001, 1, ()),
                 (0x9114, 2, (1,)), (0x9115, 3, (1,)))
        for opcode, tx, params in steps:
            result, _ = operation(command, opcode, tx, params)
            if result != PTP_SUCCESS:
                raise PTPError('Init command 0x%04X failed: 0x%04X' % (opcode, result))
        # Nonfatal discovery queries observed in a T7 capture.
        for tx, prop in ((4, 0xD1AC), (5, 0xD167)):
            operation(command, 0x9127, tx, (prop,))
        for attempt in range(6):
            time.sleep(0.2)
            status, payload = operation(command, 0x9116, attempt + 6)
            if status != PTP_SUCCESS:
                raise PTPError('EOS GetEvent failed: 0x%04X' % status)
            count = find_shutter_counter(payload)
            if count is not None:
                return count
        raise PTPError('ShutterCounter event not returned by this session.')
    finally:
        event.close()
        command.close()


def _tcp_segment(packet):
    if len(packet) < 14 or packet[12:14] != b'\x08\x00':
        return None
    ip = packet[14:]
    if len(ip) < 20 or ip[0] >> 4 != 4 or ip[9] != 6:
        return None
    ihl = (ip[0] & 15) * 4
    total = struct.unpack_from('!H', ip, 2)[0]
    if ihl < 20 or total < ihl + 20 or len(ip) < total:
        return None
    if struct.unpack_from('!H', ip, 6)[0] & 0x3FFF:
        return None
    tcp = ip[ihl:total]
    if len(tcp) < 20:
        return None
    hdr = (tcp[12] >> 4) * 4
    if hdr < 20 or hdr > len(tcp):
        return None
    sport, dport, seq = struct.unpack_from('!HHI', tcp)
    return (ip[12:16], ip[16:20], sport, dport, seq, tcp[hdr:])


def _reassemble(segments):
    """Yield uninterrupted TCP runs in sequence order."""
    buffer = []
    end = None
    for seq, data in sorted(segments.items()):
        if end is not None and seq > end:
            if buffer:
                yield b''.join(buffer)
            buffer, end = [], None
        elif end is not None and seq < end:
            data = data[end - seq:]
        if data:
            buffer.append(data)
            end = seq + len(data) if end is None else max(end, seq + len(data))
    if buffer:
        yield b''.join(buffer)


def _scan_stream(stream):
    pos = 0
    while pos + 8 <= len(stream):
        length, kind = struct.unpack_from('<II', stream, pos)
        if length < 8 or length > MAX_FRAME_SIZE or pos + length > len(stream):
            break
        if kind in (10, 12) and length >= 12:
            count = find_shutter_counter(stream[pos + 12:pos + length])
            if count is not None:
                return count
        pos += length
    return None


def read_from_pcap(path):
    """Offline classic Ethernet PCAP reader. No network connections."""
    streams = {}
    with open(path, 'rb') as fh:
        header = fh.read(24)
        if len(header) != 24:
            raise PTPError('Incomplete PCAP header.')
        magic = header[:4]
        if magic in (b'\xd4\xc3\xb2\xa1', b'\x4d\x3c\xb2\xa1'):
            endian = '<'
        elif magic in (b'\xa1\xb2\xc3\xd4', b'\xa1\xb2\x3c\x4d'):
            endian = '>'
        else:
            raise PTPError('Unsupported format: use classic PCAP, not PCAPNG.')
        if struct.unpack_from(endian + 'I', header, 20)[0] != 1:
            raise PTPError('Only Ethernet-format PCAP is supported.')
        while True:
            hdr = fh.read(16)
            if not hdr:
                break
            if len(hdr) < 16:
                raise PTPError('Truncated PCAP record header.')
            _, _, size, _ = struct.unpack(endian + 'IIII', hdr)
            if size > MAX_FRAME_SIZE:
                raise PTPError('Oversized PCAP record.')
            packet = fh.read(size)
            if len(packet) != size:
                raise PTPError('Truncated PCAP record.')
            segment = _tcp_segment(packet)
            if segment is None:
                continue
            src, dst, sport, dport, seq, payload = segment
            if sport == PTPIP_PORT and payload:
                streams.setdefault((src, dst, sport, dport), {})[seq] = payload
    for segments in streams.values():
        for data in _reassemble(segments):
            count = _scan_stream(data)
            if count is not None:
                return count
    raise PTPError('ShutterCounter property 0xD1AC not found.')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Experimental Canon EOS Wi-Fi shutter counter')
    parser.add_argument('--ip', default='192.168.1.2', help='Camera IPv4 address')
    parser.add_argument('--pcap', type=Path, help='Read an existing local PCAP file')
    parser.add_argument('--timeout', type=float, default=8)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    try:
        count = read_from_pcap(str(args.pcap)) if args.pcap else read_live(args.ip, args.timeout)
    except (OSError, PTPError) as exc:
        print('Error: %s' % exc, file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({'shutter_count': count}))
    else:
        print('Canon EOS shutter count: {:,}'.format(count))
    return 0


if __name__ == '__main__':
    sys.exit(main())
