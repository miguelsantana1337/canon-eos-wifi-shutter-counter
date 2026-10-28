"""Unit tests using synthetic data only. Never commit personal PCAP files."""
import os
import struct
import tempfile
import unittest
from unittest.mock import patch
import io
from contextlib import redirect_stdout
import canon_t7_wifi as reader


def event(value=7044, prop=reader.EOS_SHUTTER_COUNTER):
    return struct.pack('<IIII', 16, reader.EOS_PROPERTY_CHANGED, prop, value)


def ethernet_packet(data, seq=1000):
    ip = bytearray(20)
    ip[0] = 0x45
    ip[9] = 6
    ip[12:16] = bytes([192, 168, 1, 2])
    ip[16:20] = bytes([192, 168, 1, 10])
    tcp = bytearray(20)
    tcp[12] = 0x50
    struct.pack_into('!HHI', tcp, 0, 15740, 50000, seq)
    struct.pack_into('!H', ip, 2, 20 + len(tcp) + len(data))
    return bytes(12) + b'\x08\x00' + ip + tcp + data


def pcap_packet(data):
    hdr = struct.pack('<IHHIIII', 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    rec = struct.pack('<IIII', 0, 0, len(data), len(data))
    return hdr + rec + data


class ReaderTests(unittest.TestCase):
    def test_event_property(self):
        self.assertEqual(reader.find_shutter_counter(event()), 7044)

    def test_ignores_other_property(self):
        self.assertIsNone(reader.find_shutter_counter(event(prop=0xD167)))

    def test_ignores_malformed_event(self):
        self.assertIsNone(reader.find_shutter_counter(b'\x01\x02'))

    def test_frame_encode(self):
        sock = unittest.mock.Mock()
        reader.send_frame(sock, 6, b'ab')
        sock.sendall.assert_called_once_with(struct.pack('<II', 10, 6) + b'ab')

    def test_synthetic_capture(self):
        frame = struct.pack('<II', len(event()) + 12, 12) + struct.pack('<I', 9) + event()
        data = pcap_packet(ethernet_packet(frame))
        with tempfile.NamedTemporaryFile(suffix='.pcap') as fh:
            fh.write(data)
            fh.flush()
            self.assertEqual(reader.read_from_pcap(fh.name), 7044)

    def test_truncated_capture(self):
        with tempfile.NamedTemporaryFile(suffix='.pcap') as fh:
            fh.write(b'bad')
            fh.flush()
            with self.assertRaises(reader.PTPError):
                reader.read_from_pcap(fh.name)

    def test_json_cli(self):
        out = io.StringIO()
        with patch.object(reader, 'read_from_pcap', return_value=7044):
            with redirect_stdout(out):
                self.assertEqual(reader.main(['--pcap', 'fake.pcap', '--json']), 0)
        self.assertEqual(out.getvalue().strip(), '{"shutter_count": 7044}')


if __name__ == '__main__':
    unittest.main()
