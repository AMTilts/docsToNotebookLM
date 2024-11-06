import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfkit
import webbrowser

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
        if (
            absolute_url.startswith(base_url)
            and absolute_url not in visited_urls
            and '/docs/' in absolute_url  # Adjust if needed
        ):
            try:
                visited_urls.update(crawl_website(absolute_url, visited_urls))
            except RecursionError:
                print(f"Recursion depth exceeded while crawling {absolute_url}")
    return visited_urls


def get_tags(base_url, visited_urls=None):
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
    all_tags = soup.find_all()
    
    for tag in all_tags:
        print(f"Tag: {tag.name}")
        if tag.attrs:
            print(f"    Attributes: {tag.attrs}")
        if tag.string:
            print(f"    Text: {tag.string}")
        return visited_urls & all_tags
    

def scrape_and_convert_to_pdf(url, output_filename, progress_var=None):
    try:
        # Fetch the web page
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML (keeping the original formatting)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content container (corrected class name)
        content_div = soup.find("div", class_="prose")  

        if content_div:
            # Get the HTML content of the div
            html_content = str(content_div)

            # Generate the PDF using the extracted HTML
            pdfkit.from_string(html_content, output_filename)

            print(f"Successfully created PDF: {output_filename}")
        else:
            print(f"Could not find content container on {url}")

    except Exception as e:
        print(f"Error processing {url}: {e}")

    finally:
        if progress_var:
            progress_var.set(progress_var.get() + 1)
            

def start_process():
    global stop_event
    stop_event = threading.Event()
    base_url = url_entry.get()
    output_dir = output_dir_label.cget("text")
    if not base_url or not output_dir:
        return
    
    try:
        # Fetch the webpage for link extraction
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the links within the frame
        link_elements = soup.select('div > a')
        
        # Clear previous links in the frame
        for link_element in link_elements:
            link_url = urljoin(base_url, link_element['href'])
            link_text = link_element.text
            
            link_label = tk.Label(link_frame, text=link_text, foreground="blue", cursor="hand2")
            link_label.pack(anchor="w")
            
            # Bind the click event to the link
            link_label.bind("<Button-1>", lambda e, url=link_url: scrape_link(url))
            
        link_frame.pack(pady=10)
            
        start_button.config(state=tk.DISABLED)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {base_url}: {e}")
        
def scrape_link(url):
    global stop_event
    stop_event = threading.Event()
    output_dir = output_dir_label.cget("text")
    
    progress_bar.start()
    threading.Thread(target=process_single_url, args=(url, output_dir, stop_event)).start()
    
def process_single_url(url, output_dir, stop_event):
    try:
        output_filename = f"{output_dir}/documentation.pdf"
        scrape_and_convert_to_pdf(url, output_filename)
        log_text.insert(tk.END, f"{url}\n")
        log_text.see(tk.END)
        root.update_idletasks()
    finally:
        progress_bar.stop()
        
def stop_process():
    stop_event.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


def process_urls(base_url, output_dir, stop_event):
    try:
        all_urls = crawl_website(base_url)

        progress_var.set(0)
        progress_bar["maximum"] = len(all_urls)
        progress_bar.stop()
        progress_bar.config(mode="determinate")
        for i, url in enumerate(all_urls):
            if stop_event.is_set():
                break
            output_filename = f"{output_dir}/documentation_{i + 1}.pdf"
            scrape_and_convert_to_pdf(url, output_filename, progress_var)
            log_text.insert(tk.END, f"{url}\n")
            log_text.see(tk.END)
            root.update_idletasks()
        else:
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

link_frame = ttk.Frame(root)


root.mainloop()