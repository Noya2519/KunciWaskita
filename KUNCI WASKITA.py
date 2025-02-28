import os
import base64
import hashlib
import customtkinter as ctk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def generate_key(key, algo):
    return hashlib.sha256(key.encode()).digest() if algo == "AES" else hashlib.md5(key.encode()).digest()[:8]

def xor_encrypt(text, key):
    key_cycle = (key * (len(text) // len(key) + 1))[:len(text)]
    encrypted_bytes = bytes(a ^ b for a, b in zip(text.encode(), key_cycle.encode()))
    return base64.b64encode(encrypted_bytes).decode()

def xor_decrypt(text, key):
    try:
        text = base64.b64decode(text.encode())
    except Exception:
        return "Invalid XOR-encrypted text"
    key_cycle = (key * (len(text) // len(key) + 1))[:len(text)]
    decrypted_bytes = bytes(a ^ b for a, b in zip(text, key_cycle.encode()))
    return decrypted_bytes.decode(errors='ignore')

def aes_encrypt_file(filename, key):
    key = generate_key(key, "AES")
    iv = key[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
    new_filename = filename + ".enc"
    with open(new_filename, "wb") as file:
        file.write(encrypted_data)
    return new_filename

def aes_decrypt_file(filename, key):
    key = generate_key(key, "AES")
    iv = key[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(filename, "rb") as file:
        file_data = file.read()
    decrypted_data = unpad(cipher.decrypt(file_data), AES.block_size)
    new_filename = filename.replace(".enc", "")
    with open(new_filename, "wb") as file:
        file.write(decrypted_data)
    return new_filename

class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Encryption & Decryption App")
        self.geometry("500x600")
        
        self.configure(bg="#0a0f25")

        self.label = ctk.CTkLabel(self, text="Pilih file atau masukkan teks:", text_color="white")
        self.label.pack(pady=5)
        
        self.text_entry = ctk.CTkTextbox(self, height=100, width=400)
        self.text_entry.pack(pady=5)
        
        self.file_button = ctk.CTkButton(self, text="Pilih File", command=self.select_file, fg_color="#1e3a8a")
        self.file_button.pack(pady=5)
        
        self.key_label = ctk.CTkLabel(self, text="Masukkan kunci:", text_color="white")
        self.key_label.pack(pady=5)
        self.key_entry = ctk.CTkEntry(self, show="*")
        self.key_entry.pack(pady=5)
        
        self.method_var = ctk.StringVar(value="AES")
        self.method_menu = ctk.CTkComboBox(self, variable=self.method_var, values=["AES", "DES", "XOR"], fg_color="#1e3a8a")
        self.method_menu.pack(pady=5)
        
        self.encrypt_button = ctk.CTkButton(self, text="Enkripsi", command=self.encrypt, fg_color="#1e3a8a")
        self.encrypt_button.pack(pady=5)
        
        self.decrypt_button = ctk.CTkButton(self, text="Dekripsi", command=self.decrypt, fg_color="#1e3a8a")
        self.decrypt_button.pack(pady=5)
        
        self.result_label = ctk.CTkLabel(self, text="Hasil:", text_color="white")
        self.result_label.pack(pady=5)
        self.result_text = ctk.CTkTextbox(self, height=100, width=400)
        self.result_text.pack(pady=5)
        
        self.selected_file = None
    
    def select_file(self):
        self.selected_file = filedialog.askopenfilename()
        if self.selected_file:
            messagebox.showinfo("File Dipilih", f"File: {self.selected_file}")
    
    def encrypt(self):
        key = self.key_entry.get()
        method = self.method_var.get()
        if not key:
            messagebox.showerror("Error", "Kunci harus diisi!")
            return
        if self.selected_file:
            try:
                if method == "AES":
                    output_file = aes_encrypt_file(self.selected_file, key)
                messagebox.showinfo("Sukses", f"File terenkripsi: {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengenkripsi: {str(e)}")
        else:
            text = self.text_entry.get("1.0", "end").strip()
            if not text:
                messagebox.showerror("Error", "Masukkan teks atau pilih file!")
                return
            if method == "XOR":
                result = xor_encrypt(text, key)
            else:
                messagebox.showerror("Error", "Hanya XOR yang didukung untuk teks langsung.")
                return
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", result)
    
    def decrypt(self):
        key = self.key_entry.get()
        method = self.method_var.get()
        if not key:
            messagebox.showerror("Error", "Kunci harus diisi!")
            return
        if self.selected_file:
            try:
                if method == "AES":
                    output_file = aes_decrypt_file(self.selected_file, key)
                messagebox.showinfo("Sukses", f"File didekripsi: {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mendekripsi: {str(e)}")
        else:
            text = self.text_entry.get("1.0", "end").strip()
            if not text:
                messagebox.showerror("Error", "Masukkan teks atau pilih file!")
                return
            if method == "XOR":
                result = xor_decrypt(text, key)
            else:
                messagebox.showerror("Error", "Hanya XOR yang didukung untuk teks langsung.")
                return
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", result)

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()
