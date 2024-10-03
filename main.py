import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfkit
def crawl_website(base_url, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()

    visited_urls.add(base_url)
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {base_url}: {e}")
        return visited_urls

    soup = BeautifulSoup(response.content, 'html.parser')

    for link in soup.find_all('a', href=True):
        absolute_url = urljoin(base_url, link['href'])
        if absolute_url.startswith(base_url) and absolute_url not in visited_urls and '/docs/' in absolute_url:
            try:
                visited_urls.update(crawl_website(absolute_url, visited_urls))
            except RecursionError:
                print(f"Recursion depth exceeded while crawling {absolute_url}")
    return visited_urls

def scrape_and_convert_to_pdf(url, output_filename, progress_var):
    try:
        # Fetch the web page
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract relevant content (example)
        title = soup.find('h1').text
        heading = soup.find('h2').text
        content = soup.find('div', class_='content').text

        # Structure the content for the PDF (example)
        html_template = f"""
        <h1>{title}</h1>
        <h2>{heading}</h2>
        <p>{content}</p>
    """
        # Generate the PDF
        pdfkit.from_string(html_template, output_filename)

    except Exception as e:
        print(f"Error processing {url}: {e}")
    finally:
        progress_var.set(progress_var.get() + 1)

def start_process():
    global stop_event
    stop_event = threading.Event()
    base_url = url_entry.get()
    output_dir = output_dir_label.cget("text")  # Get output directory from label
    if not base_url or not output_dir:
        return

    progress_bar.start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    threading.Thread(target=process_urls, args=(base_url, output_dir, stop_event)).start()

def stop_process():
    stop_event.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def process_urls(base_url, output_dir, stop_event):
    try:
        all_urls = crawl_website(base_url)
        progress_var.set(0)
        progress_bar["maximum"] = len(all_urls)
        progress_bar.stop()  # Stop indeterminate mode
        progress_bar.config(mode="determinate")  # Switch to determinate mode
        for i, url in enumerate(all_urls):
            if stop_event.is_set():
                break
            output_filename = f"{output_dir}/documentation_{i + 1}.pdf"
            scrape_and_convert_to_pdf(url, output_filename, progress_var)
            log_text.insert(tk.END, f"Processed: {url}\n")
            log_text.see(tk.END)  # Scroll to the end
            root.update_idletasks()  # Update the GUI
        else:  # If the loop completes without interruption
            messagebox.showinfo("Scraping Complete", f"Scraping complete!\nFiles saved to:\n{output_dir}")
    finally:
        progress_bar.stop()
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def select_output_directory():
    output_dir = filedialog.askdirectory()
    if output_dir:
        output_dir_label.config(text=output_dir)

# Set up the main application window
root = tk.Tk()
root.title("Documentation Scraper")

# URL input
url_label = ttk.Label(root, text="Enter the base URL:")
url_label.pack(pady=10)
url_entry = ttk.Entry(root, width=50)
url_entry.pack()

# Output directory selection
output_dir_label = ttk.Label(root, text="No directory selected")
output_dir_label.pack(pady=5)
output_button = ttk.Button(root, text="Select Output Directory", command=select_output_directory)
output_button.pack(pady=5)

# Start and Stop buttons
start_button = ttk.Button(root, text="Start Scraping", command=start_process)
start_button.pack(pady=10)
stop_button = ttk.Button(root, text="Stop Scraping", command=stop_process, state=tk.DISABLED)
stop_button.pack(pady=10)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", variable=progress_var)
progress_bar.pack(pady=10)

# Log section
log_label = ttk.Label(root, text="Log:")
log_label.pack()
log_text = tk.Text(root, wrap=tk.WORD, height=10, width=50)
log_text.pack(pady=10)

root.mainloop()