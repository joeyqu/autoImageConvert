# Auto Image Convert

This script monitors a directory for new image files and automatically converts them to PNG format. It uses the `watchdog` library to detect file system events, such as file creation and file movement. When a new image file is detected, it is opened using the `PIL` (Python Imaging Library) module, and if the image format is not already PNG, it is converted to PNG format and saved with the same filename but with the `.png` extension. The original image file is then removed.

## Prerequisites

- Python 3.x
- `PIL` library (`pip install pillow`)
- `watchdog` library (`pip install watchdog`)
- `pystray` library (`pip install pystray`)

## Usage

1. Clone or download the repository.
2. Install the required libraries using the command `pip install -r requirements.txt`.
3. Modify the `config.json` file to specify the directory to monitor and the preferred text editor for configuration.
4. Run the script using the command `python auto_image_convert.py`.
5. The script will start monitoring the specified directory for new image files and automatically convert them to PNG format.

## Configuration

The script uses a `config.json` file to store the configuration settings. The file should be placed in the same directory as the script. The following options can be configured:

- `listen_dir`: The directory to monitor for new image files. If not specified, the default directory is `~/Downloads`.
- `config_editor`: The text editor to open the `config.json` file for editing. If not specified, the default editor is `notepad`.

To open the `config.json` file for editing, right-click on the system tray icon and select "Configuration". Make the necessary changes and save the file.

## System Tray Icon

The script uses the `pystray` library to display a system tray icon. Right-clicking on the icon provides options to open the configuration file or quit the application.

## License

This script is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
