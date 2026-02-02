# process_one.py
from __future__ import annotations
import argparse

from io_wav import read_wav, write_wav
from echo import apply_echo
from time_stretch import apply_time_stretch
from pitch_shift import pitch_shift

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input_wav")
    p.add_argument("output_wav")

    p.add_argument("--echo", action="store_true")
    p.add_argument("--delay", type=float, default=0.25)
    p.add_argument("--decay", type=float, default=0.35)

    p.add_argument("--tempo", type=float, default=1.0, help=">1.0 slower, <1.0 faster (stretch factor)")
    p.add_argument("--pitch", type=float, default=0.0, help="semitones, e.g. +3, -5")

    args = p.parse_args()

    x, sr = read_wav(args.input_wav)
    y = x

    if args.echo:
        y = apply_echo(y, sr, delay_sec=args.delay, decay=args.decay)

    if args.tempo != 1.0:
        y = apply_time_stretch(y, sr, stretch=args.tempo)

    if args.pitch != 0.0:
        y = pitch_shift(y, semitones=args.pitch, sr=sr)

    write_wav(args.output_wav, y, sr)
    print(f"Saved: {args.output_wav}")

if __name__ == "__main__":
    main()
