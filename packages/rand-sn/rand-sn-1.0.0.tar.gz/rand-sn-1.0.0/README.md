# Project Name
# rand-sn - Random Serial Number Generator

## Description

This Python tool generates serial numbers, corresponding barcodes, and QR codes, making it ideal for secure labelling and easy scanning. It allows you to assign serial numbers to batches of physical objects, enhancing inventory management and product tracking. A standout feature of this tool is its ability to randomize the order of serial numbers, effectively masking the total quantity of items produced. The program is handy for maintaining operational confidentiality by preventing estimates of production volumes. For a closer look at the tool's capabilities, please refer to our output [samples](samples).
- The program uses a config file to resume where the last batch ended.
- Each batch is stored in a sequentially numbered subdirectory.
- The file serial-numbers.json contains a list of all in the batch. Many tools can import .json files.
- Bar files are rectangular barcode images. These are best when space is limited.
- QR files are square QR code images. If you want to create a dedicated web page for each object, you can embed a URL starter in the QR code. They can take the place of a printed manual.
- You can resize the images to match the DPI of your printer and the expected scanner resolution.

## Installation
Instructions on how to install and configure the project are incomplete; you can do the following for now:
1. Install the current stable version of [Python](https://www.python.org). 
2. At the command line or terminal prompt, enter.
```bash
pip install rand-sn
```

## Upgrade
At the command line or terminal prompt, enter.
```bash
pip install --upgrade rand-sn
```

## Usage
A guide on how to use the project.

### Configuration

Begin by deciding how you want serial numbers to be. For each config file, do this once and only once. The command-line options are as follows:
- `-s` or `--smallest`: The lowest possible serial number. The default 1. 
- `-b` or `--biggest`: The highest possible serial number. There is no default.
- `-p` or `--prefix`: A prefix added to the start of every QR code. None is the default.
- `-c` or `--config`: The optional config file's name.

Sample command:
```rand-sn -b 9999 -p https://your-domain.com/serial-number/```

### Batching
After configuring, generate a new batch of serial numbers every time you need one. The command-line options are as follows:
- `-n` or `--number`: You need serial numbers in the new batch. There is no default.
- `-c` or `--config`:  The optional config file's name.

Sample command:
```rand-sn -n 10```

## Backup and Restore

Back up after each batch or use an automated backup solution; highly recommended

The config file (code-QR-generator-config.json by default) determines the following serial numbers and is crucial for the tool to function correctly. Make sure to back it up regularly.

To recover, reinstall the program and restore the config file to its working directory.

### FAQ

---

**Q:** When I run rand-sn my operating system says something like command not found.

**A:** Try this alternative.
        ```
        python3 -m rand-sn
        ```
---

**Q:** Can I configure and generate batches at the same time?

**A:** Configuration and batch generation are two separate processes. Initially, you must configure the system once for your setup. After configuration, you can generate batches of serial numbers as needed. This approach ensures that each batch adheres to the predefined configuration, maintaining consistency across your serial numbers.

---

**Q:** Can I edit my config file if I change my mind about the configuration settings?

**A:** You can safely edit the QR code prefix directly within your configuration file. For other settings, particularly those affecting the range and format of serial numbers, it's recommended to create a new configuration file to avoid inconsistencies or conflicts with previously generated batches.

---

**Q:** How can I manage multiple products?

**A:** For handling multiple products, utilize the `-c` or `--config` option to create and specify a unique configuration file for each product. This method allows you to maintain distinct settings for each product line, ensuring that each product's identifiers are specific and organized.

---

**Q:** How do I avoid leading zeros in serial numbers?

**A1:** To prevent leading zeros, carefully set the `-s` (smallest) and `-b` (biggest) options to define the range of your serial numbers. Adjust the range according to the total number of serial numbers you anticipate needing. For instance, if you expect to require up to 5000 serial numbers, you might set your range from 1000 to 9999, giving you ample space for expansion.

**A2:** For those utilizing barcodes, please refer to the following question for additional guidance.

---

**Q:** Why do all my barcodes start with a zero?

**A:** Barcodes encode numbers in pairs. Use an even number of digits in your serial numbers to avoid the automatic leading zero.

---

**Q:** During manual entry, how can I detect data entry errors?

**A1:** See earlier about avoiding leading zeros. Verify the length of each entered number.

**A2:** Maintain a database of all generated serial numbers. Use it to do real-time validation.

**A3:** Currently, the system does not offer an option to include a check digit in serial numbers. Incorporating a check digit can significantly reduce data entry errors by allowing for immediate validation of each serial number's correctness.

---

**Q:** Will the system alert me if I've exhausted all possible serial numbers?

**A:** Yes, batch generation will abort when the potential for generating new, unique serial numbers within the configured range is exhausted. Planning your serial number ranges and configurations with future needs is essential.

---

## License

This project is distributed under the [MIT License](LICENSE.txt).

## Contact

If you find room for improvement or need to ask a question, open a new [issue](https://github.com/matecsaj/rand_sn/issues). 

If you are a Python programmer or a writer and want to contribute, see [CONTRIBUTING.md](CONTRIBUTING.md).

For inquiries, please contact: Peter JOHN Matecsa
matecsaj@gmail.com
