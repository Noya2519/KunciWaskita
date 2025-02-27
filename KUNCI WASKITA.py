import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
import base64
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CryptoApp")
        self.geometry("600x500")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_tab = self.tabview.add("Enkripsi Teks")
        self.file_tab = self.tabview.add("Enkripsi File")

        self.text_crypto_ui()
        self.file_crypto_ui()


    def text_crypto_ui(self):
        ctk.CTkLabel(self.text_tab, text="Masukkan Teks:").pack(pady=5)
        self.text_input = ctk.CTkEntry(self.text_tab, width=400)
        self.text_input.pack(pady=5)

        self.key_input = ctk.CTkEntry(self.text_tab, placeholder_text="Masukkan Kunci", width=400, show="*")
        self.key_input.pack(pady=5)

        self.method_var = tk.StringVar(value="XOR")
        self.method_menu = ctk.CTkOptionMenu(self.text_tab, variable=self.method_var, values=["XOR", "AES", "DES"])
        self.method_menu.pack(pady=5)

        ctk.CTkButton(self.text_tab, text="Enkripsi", command=self.encrypt_text).pack(pady=5)
        ctk.CTkButton(self.text_tab, text="Dekripsi", command=self.decrypt_text).pack(pady=5)

        self.result_label = ctk.CTkLabel(self.text_tab, text="Hasil akan muncul di sini")
        self.result_label.pack(pady=5)


    def file_crypto_ui(self):
        ctk.CTkLabel(self.file_tab, text="Pilih file untuk enkripsi").pack(pady=5)
        ctk.CTkButton(self.file_tab, text="Pilih File", command=self.select_file).pack(pady=5)

        self.file_key_input = ctk.CTkEntry(self.file_tab, placeholder_text="Masukkan Kunci", width=400, show="*")
        self.file_key_input.pack(pady=5)

        self.file_method_var = tk.StringVar(value="AES")
        self.file_method_menu = ctk.CTkOptionMenu(self.file_tab, variable=self.file_method_var, values=["AES", "DES"])
        self.file_method_menu.pack(pady=5)

        ctk.CTkButton(self.file_tab, text="Enkripsi File", command=self.encrypt_file).pack(pady=5)
        ctk.CTkButton(self.file_tab, text="Dekripsi File", command=self.decrypt_file).pack(pady=5)

        self.selected_file = None


    def select_file(self):
        self.selected_file = filedialog.askopenfilename()
        if self.selected_file:
            messagebox.showinfo("File Dipilih", f"File: {self.selected_file}")


    def encrypt_text(self):
        text = self.text_input.get()
        key = self.key_input.get()
        method = self.method_var.get()
        if method == "AES":
            result = self.aes_encrypt_text(text, key)
        elif method == "DES":
            result = self.des_encrypt_text(text, key)
        else:
            result = self.xor_encrypt(text, key)
        self.result_label.configure(text=f"Hasil: {result}")

    def decrypt_text(self):
        text = self.text_input.get()
        key = self.key_input.get()
        method = self.method_var.get()
        if method == "AES":
            result = self.aes_decrypt_text(text, key)
        elif method == "DES":
            result = self.des_decrypt_text(text, key)
        else:
            result = self.xor_encrypt(text, key)
        self.result_label.configure(text=f"Hasil: {result}")


    def encrypt_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Pilih file terlebih dahulu!")
            return

        key = self.file_key_input.get().ljust(16, '0')[:16].encode()
        method = self.file_method_var.get()

        # Ambil ekstensi file asli
        ext = os.path.splitext(self.selected_file)[1].encode()

        with open(self.selected_file, 'rb') as f:
            data = f.read()

        save_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted Files", "*.enc")])
        if not save_path:
            return

        if method == "AES":
            cipher = AES.new(key, AES.MODE_CBC, key)
        else:  # DES
            key = key[:8]
            cipher = DES.new(key, DES.MODE_CBC, key)

        encrypted_data = cipher.encrypt(pad(ext + data, AES.block_size))

        with open(save_path, 'wb') as f:
            f.write(cipher.iv + encrypted_data)  # Simpan IV

        messagebox.showinfo("Sukses", f"File berhasil dienkripsi!\nDisimpan di: {save_path}")

    def decrypt_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Pilih file terlebih dahulu!")
            return

        key = self.file_key_input.get().ljust(16, '0')[:16].encode()
        method = self.file_method_var.get()

        with open(self.selected_file, 'rb') as f:
            iv = f.read(16)  # Baca IV
            encrypted_data = f.read()

        if method == "AES":
            cipher = AES.new(key, AES.MODE_CBC, iv)
        else:  # DES
            key = key[:8]
            cipher = DES.new(key, DES.MODE_CBC, iv)

        try:
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        except ValueError:
            messagebox.showerror("Error", "Dekripsi gagal! Kunci salah atau file rusak.")
            return


        ext_len = decrypted_data.find(b'.')
        if ext_len == -1:
            ext = b''
        else:
            ext = decrypted_data[:ext_len+4]  
            decrypted_data = decrypted_data[ext_len+4:]

   
        save_path = filedialog.asksaveasfilename(defaultextension=ext.decode(), filetypes=[("Original File", f"*{ext.decode()}")])
        if not save_path:
            return

        with open(save_path, 'wb') as f:
            f.write(decrypted_data)

        messagebox.showinfo("Sukses", f"File berhasil didekripsi!\nDisimpan di: {save_path}")

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()
