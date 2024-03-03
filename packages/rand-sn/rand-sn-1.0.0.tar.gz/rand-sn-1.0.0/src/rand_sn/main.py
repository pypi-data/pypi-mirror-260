# python

# standard libraries
from argparse import ArgumentParser, Namespace
import json
import os
from typing import Any, Dict, Optional, Tuple

# 3rd party libraries
import barcode      # unconventional, instead of barcode, python-barcode must be installed
from barcode.writer import ImageWriter
import qrcode

# local libraries
try:
    # attempt relative import (assuming running as part of a package)
    from .batch import Batch
    from .config import Config
    from .full_cycle_random import FullCycleRandom
except ImportError:
    # fallback to absolute import (assuming running as standalone script)
    from batch import Batch
    from config import Config
    from full_cycle_random import FullCycleRandom


def generate_barcode(number: int, path: str) -> None:
    """
    Generate a barcode using Code 128C format.

    Args:
        number (int): the number that should be in the barcode
        path (str): the path where the barcode should be stored

    Returns:
        None
    """
    # Choose the barcode format
    barcode_format = 'code128'

    # Ensure the number is positive and pad with a leading zero if the length is odd
    if not isinstance(number, int) or number < 0:
        raise ValueError("number argument must be a positive integer.")
    data = str(number)
    if len(data) % 2 != 0:
        data = '0' + data  # Pad with leading zero if necessary

    # Adjustments for the ImageWriter
    options = {
        'module_width': 0.2,
        'module_height': 15.0,
        'quiet_zone': 6.5,
        'text_distance': 5.0,
        'font_size': 10,
        'background': 'white',
        'foreground': 'black',
    }

    # Create the ImageWriter with options
    writer = barcode.writer.ImageWriter()

    # Apply writer options directly to the writer instance
    # Note: This step is adjusted to correctly use the writer instance with options
    writer_options = options  # This line is not needed; options are passed directly to the writer in the save method

    # Create the barcode object without passing writer_options
    code128_class = barcode.get_barcode_class(barcode_format)
    code128 = code128_class(data, writer=writer)

    # Save the barcode as an image with writer options
    output_filename = f"bar{number}"
    code128.save(os.path.join(path, output_filename), options=writer_options)


def generate_qrcode(number: int, path: str, prefix: Optional[str]) -> None:
    """
    Generate a QR code.

    Args:
        number (int): the number that should be in the barcode
        prefix (str): what should be put before the number in the QR code, example, https://mydomain.com/c/.
        path (str): the path where the barcode should be stored

    Returns:
        None
    """

    # Generate QR code
    qr = qrcode.QRCode(
        # version=1,      # size 1(small) to 40(large) or omit and use fit=True for auto
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,    # the size of each box (pixel) in the QR code
        border=4,       # recommended minimum is 4
    )
    if prefix is not None:
        data = f"{prefix}{number}"
    else:
        data = str(number)
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save(os.path.join(path, f"qr{number}.png"))


def validate_args() -> Tuple[bool, Namespace]:
    """
    Validates the command line arguments and returns the results.
    This function is called after parsing the arguments with argparse.

    Args:
        args: The namespace object returned by argparse.parse_args().

    Returns:
        A tuple with validated arguments or raises an error with help messages.
    """
    parser = ArgumentParser(description="rand-sn - A tool for generating randomized serial numbers with bar and QR codes.")

    # Common arguments, don't use a default= param, it will be added later
    parser.add_argument("-c", "--config", type=str,
                        help="The name of the config file. Default is 'rand-sn-config'.")

    # Configuration mode arguments
    parser.add_argument("-s", "--smallest", type=int,
                        help="The smallest possible serial number. Default is 1.")
    parser.add_argument("-b", "--biggest", type=int,
                        help="The biggest possible serial number. There is no default.")
    parser.add_argument("-p", "--prefix", type=str,
                        help="A prefix added to the start of every QR code. There is no default.")

    # Batching mode arguments
    parser.add_argument("-n", "--number", type=int,
                        help="The number of serial numbers you need in the new batch.")

    # Parse the command line arguments
    args = parser.parse_args()

    # Validate and process the arguments
    if args.smallest is not None and args.smallest < 1:
        raise ValueError("The smallest serial number must be greater than 0.")
    if args.biggest is not None and args.biggest <= args.smallest:
        raise ValueError("The biggest serial number must be greater than the smallest serial number.")
    if args.number is not None and args.number < 1:
        raise ValueError("The number of serial numbers must be greater than 0.")

    # Check if we're in configuration mode or batching mode based on provided arguments.
    if args.smallest is not None or args.biggest is not None or args.prefix is not None:
        config_mode = True
    elif args.number is not None:
        config_mode = False
    else:
        parser.print_help()
        exit()

    return config_mode, args


def configure(args: Namespace) -> None:
    """
    Create a configuration file.

    Args:
        args: The namespace object returned by argparse.parse_args().

    Returns:
        None or raises an error.
    """
    config = Config(config_filename=args.config)
    config.configure(smallest=args.smallest, biggest=args.biggest, prefix=args.prefix)
    config.save()
    print(f"Configured successfully. Important, keep this backed up: {config.path_file}")


def next_batch(args: Namespace) -> None:
    """
    Generate the next batch of serial numbers, barcodes and QR codes.

    Args:
        args: The namespace object returned by argparse.parse_args().

    Returns:
        None or raises an error.
    """
    # preparation
    config = Config(config_filename=args.config)
    config.load()
    fcr = FullCycleRandom(min_int=config.smallest, seed=config.seed, max_int=config.biggest)
    batch = Batch()

    # proceed, but if anything goes wrong delete the batch, otherwise save the new seed
    try:
        # for each new serial number generate a bar and QR code
        serial_numbers: list[int] = []
        for _ in range(args.number):
            number = next(fcr)
            config.seed_cycle(number)   # update the seed and check for overflow
            serial_numbers.append(number)
            generate_barcode(number, batch.path_directory)
            generate_qrcode(number, batch.path_directory, config.prefix)

        # store all new serial numbers in a file
        with open(os.path.join(batch.path_directory, 'serial-numbers.json'), 'w') as f:
            json.dump(serial_numbers, f, indent=4)

    # No matter what went wrong, delete the incomplete batch.
    except Exception as e:
        batch.delete()  # Call the delete method
        raise   # re-raise, let the caller know what went wrong

    # All went well, save the config, so the next batch continues the sequence.
    else:
        config.save()
        print(f"Batch {batch.number} generated {args.number} serial numbers. Look here: {batch.path_directory}")


def main() -> None:
    """
    The main function.

    Either configuration information or a new batch of serials numbers are written to disk.
    A config must precede batches.

    Args:
        Command line arguments.

    Returns:
        None or raises an error.
    """
    config_mode, validated_args = validate_args()
    if config_mode:
        configure(validated_args)
    else:
        next_batch(validated_args)


if __name__ == "__main__":
    main()
