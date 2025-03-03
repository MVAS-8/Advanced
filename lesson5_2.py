import os
import time
import threading

def watch_file(filename, event):
    while not event.is_set():
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()
                if "Wow!" in content:
                    print("Рядок 'Wow!' знайдено! Генеруємо подію...")
                    event.set()
                    return
                else:
                    print("Файл знайдено, але рядка 'Wow!' немає. Чекаємо 5 секунд...")
        else:
            print("Файл не знайдено. Чекаємо 5 секунд...")
        time.sleep(5)

def delete_file(filename, event):
    event.wait()
    if os.path.exists(filename):
        os.remove(filename)
        print("Файл видалено після знаходження 'Wow!'")
    else:
        print("Файл вже не існує.")

def main():
    filename = "testfile.txt"
    event = threading.Event()
    
    watcher_thread = threading.Thread(target=watch_file, args=(filename, event))
    deleter_thread = threading.Thread(target=delete_file, args=(filename, event))
    
    watcher_thread.start()
    deleter_thread.start()
    
    watcher_thread.join()
    deleter_thread.join()

if __name__ == "__main__":
    main()