import os
import sys
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import sleep
from pystray import MenuItem as item
import pystray
import json
# Get the current directory

def load_config():
  # Check if config.json exists
  if os.path.exists("config.json"):
    # Read the config file
    with open("config.json", "r") as f:
      config = json.load(f)
    # Get the listen_dir from the config file
    listen_dir = config.get("listen_dir")
    # Get the config_editor from the config file
    config_editor = config.get("config_editor")
    # Get the script_dir from the config file if not null
    if listen_dir:
      script_dir = listen_dir
    # Get the config_editor from the config file if not null
    if config_editor:
      config_editor_path = config_editor
  else:
    script_dir = os.path.expanduser("~/Downloads")

  return script_dir, config_editor_path


def openConfig(config_editor="notepad"):
    os.system(f"{config_editor} config.json")
    
def closeApp():
    os._exit(0)


class NewFileHandler(FileSystemEventHandler):
  def on_moved(self, event):
    sleep(3)
    print('file moved ' + event.src_path)
    if not event.is_directory and '.png' not in event.src_path:
      
      filepath = event.src_path[:-11]
      print(filepath)
      filename = "\\".join(filepath.split('\\')[-1:])
    
      if filename.endswith(('.jpg', '.jpeg', '.gif', '.png', '.bmp', '.tiff','.webp')):
        # Open the image file
        image = Image.open(filepath)
        # Convert the image to PNG format
        if image.format != 'PNG':
          new_filename = os.path.splitext(filepath)[0] + '.png'
          image.save(new_filename, 'PNG')
        # Close the image file
        image.close()
        # Remove the original image file
        os.remove(filename)
        
  def on_created(self, event):
    print('file created ' + event.src_path)
    if not event.is_directory and '.png' not in event.src_path and '.crdownload' not in event.src_path:
      
      filepath = event.src_path[:-11]
      print(filepath)
      filename = "\\".join(filepath.split('\\')[-1:])
    
      if filename.endswith(('.jpg', '.jpeg', '.gif', '.png', '.bmp', '.tiff','.webp')):
        # Open the image file
        image = Image.open(filepath)
        # Convert the image to PNG format
        if image.format != 'PNG':
          new_filename = os.path.splitext(filepath)[0] + '.png'
          image.save(new_filename, 'PNG')
        # Close the image file
        image.close()
        # Remove the original image file
        os.remove(filename)
 


if __name__ == '__main__':
  script_dir, config_editor_path = load_config()
  
  icon_folder = os.path.join(sys._MEIPASS, 'static')
  image = Image.open("icons/favicon.ico")
  menu = (item('Configuration', openConfig), item('Quit', closeApp))
  icon = pystray.Icon("name", image, "MyApp Name", menu)

  icon.run()
  print('script loaded, listening for new files in ' + script_dir)
  # Create an observer and attach the event handler
  observer = Observer()
  observer.schedule(NewFileHandler(), script_dir, recursive=True)
  observer.start()
  try:
    while True:
      # Keep the program running
      pass
  except KeyboardInterrupt:
    observer.stop()
  observer.join()
  
icon_folder = os.path.join(sys._MEIPASS, 'static')
image = Image.open("icons/favicon.ico")
menu = (item('Configuration', openConfig), item('Quit', closeApp))
icon = pystray.Icon("name", image, "MyApp Name", menu)

icon.run()
print('script loaded, listening for new files in ' + script_dir)
# Create an observer and attach the event handler
observer = Observer()
observer.schedule(NewFileHandler(), script_dir, recursive=True)
observer.start()
try:
  while True:
    # Keep the program running
    pass
except KeyboardInterrupt:
  observer.stop()
observer.join()

