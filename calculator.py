import tkinter as tk
from tkinter import messagebox

class KalkulatorDesktopModern:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Desktop")
        
        # Ukuran awal jendela
        self.root.geometry("380x580")
        self.root.minsize(300, 450)
        self.root.resizable(True, True)
        
        # Palet Warna Utama
        self.BG_MAIN = "#17171C"       
        self.BG_DISPLAY = "#22222A"    
        self.BTN_NUM = "#2E2F38"       
        self.TXT_PRIMARY = "#FFFFFF"   

        # Warna Latar Belakang Penuh (Full Background) dan Teks untuk Setiap Tanda/Operator
        # Format: "TANDA": (Warna_Background, Warna_Teks)
        self.COLOR_SIGNS = {
            "C": ("#E74C3C", "#FFFFFF"),    # Merah Penuh
            "⌫": ("#E67E22", "#FFFFFF"),   # Oranye Penuh
            "%": ("#F1C40F", "#17171C"),    # Kuning Penuh
            "÷": ("#2980B9", "#FFFFFF"),    # Biru Tua Penuh
            "×": ("#16A085", "#FFFFFF"),    # Toska Penuh
            "-": ("#C0392B", "#FFFFFF"),    # Merah Gelap Penuh
            "+": ("#27AE60", "#FFFFFF"),    # Hijau Penuh
            "(": ("#8E44AD", "#FFFFFF"),    # Ungu Penuh
            ")": ("#9B59B6", "#FFFFFF"),    # Ungu Muda Penuh
            "±": ("#3498DB", "#FFFFFF"),    # Biru Muda Penuh
            "=": ("#4B5EAA", "#FFFFFF")     # Indigo/Accent Penuh
        }

        self.root.configure(bg=self.BG_MAIN)
        self.ekspresi = ""

        # --- Display Frame ---
        frame_layar = tk.Frame(self.root, bg=self.BG_DISPLAY, bd=0, highlightthickness=1, highlightbackground="#2E2F38")
        frame_layar.pack(fill="both", padx=20, pady=(20, 15), ipady=10)

        self.label_sub = tk.Label(
            frame_layar,
            text="",
            anchor="e",
            bg=self.BG_DISPLAY,
            fg="#8E8E93",
            font=("Segoe UI", 12),
            padx=15
        )
        self.label_sub.pack(fill="x")

        self.label_layar = tk.Label(
            frame_layar,
            text="0",
            anchor="e",
            bg=self.BG_DISPLAY,
            fg=self.TXT_PRIMARY,
            font=("Segoe UI", 32, "bold"),
            padx=15
        )
        self.label_layar.pack(fill="x")

        # --- Tombol Frame ---
        frame_tombol = tk.Frame(self.root, bg=self.BG_MAIN)
        frame_tombol.pack(expand=True, fill="both", padx=15, pady=(0, 20))

        tombol_layout = [
            ["C", "⌫", "%", "÷"],
            ["(", ")", "±", "×"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "="],
            ["0", "."]
        ]

        for i in range(6):
            frame_tombol.rowconfigure(i, weight=1)
        for j in range(4):
            frame_tombol.columnconfigure(j, weight=1)

        for baris_idx, baris in enumerate(tombol_layout):
            for kolom_idx, teks in enumerate(baris):
                
                # Menentukan warna tombol berdasarkan jenisnya
                if teks in self.COLOR_SIGNS:
                    bg_col, fg_col = self.COLOR_SIGNS[teks]
                    active_bg = bg_col  # Menjaga warna tetap konsisten saat ditekan
                else:
                    bg_col, fg_col = self.BTN_NUM, self.TXT_PRIMARY
                    active_bg = "#505160"

                btn = tk.Button(
                    frame_tombol,
                    text=teks,
                    font=("Segoe UI", 16, "bold"),
                    bg=bg_col,
                    fg=fg_col,
                    activebackground=active_bg,
                    activeforeground=fg_col,
                    bd=0,
                    relief="flat",
                    cursor="hand2",
                    command=lambda val=teks: self.tekan_tombol(val)
                )

                if teks == "=":
                    btn.grid(row=4, column=3, rowspan=2, sticky="nsew", padx=4, pady=4)
                elif teks == "0":
                    btn.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)
                elif teks == ".":
                    btn.grid(row=5, column=2, sticky="nsew", padx=4, pady=4)
                else:
                    btn.grid(row=baris_idx, column=kolom_idx, sticky="nsew", padx=4, pady=4)

        self.root.bind("<Key>", self.input_keyboard)

    def tekan_tombol(self, nilai):
        if nilai == "C":
            self.ekspresi = ""
            self.label_sub.config(text="")
            self.update_layar("0")
            
        elif nilai == "⌫":
            self.ekspresi = self.ekspresi[:-1]
            self.update_layar(self.ekspresi if self.ekspresi else "0")
            
        elif nilai == "%":
            if self.ekspresi:
                try:
                    ekspresi_eval = self.proses_ekspresi(self.ekspresi)
                    hasil = eval(ekspresi_eval) / 100
                    if isinstance(hasil, float) and hasil.is_integer():
                        hasil = int(hasil)
                    self.ekspresi = str(hasil)
                    self.update_layar(self.ekspresi)
                except Exception:
                    self.tampilkan_error("Format Persen Salah")

        elif nilai == "=":
            self.hitung_hasil()
            
        elif nilai == "±":
            if self.ekspresi:
                if self.ekspresi.startswith("-"):
                    self.ekspresi = self.ekspresi[1:]
                else:
                    self.ekspresi = "-" + self.ekspresi
                self.update_layar(self.ekspresi)
                
        else:
            self.ekspresi += str(nilai)
            self.update_layar(self.ekspresi)

    def proses_ekspresi(self, teks):
        return teks.replace("×", "*").replace("÷", "/")

    def hitung_hasil(self):
        try:
            if not self.ekspresi:
                return
            
            self.label_sub.config(text=self.ekspresi + " =")
            ekspresi_eval = self.proses_ekspresi(self.ekspresi)
            hasil = eval(ekspresi_eval)
            
            if isinstance(hasil, float) and hasil.is_integer():
                hasil = int(hasil)

            self.ekspresi = str(hasil)
            self.update_layar(self.ekspresi)

        except ZeroDivisionError:
            self.tampilkan_error("Tidak bisa bagi 0")
        except Exception:
            self.tampilkan_error("Ekspresi Tak Valid")

    def tampilkan_error(self, pesan):
        messagebox.showerror("Error Matematika", pesan)
        self.ekspresi = ""
        self.label_sub.config(text="")
        self.update_layar("0")

    def update_layar(self, teks):
        if len(teks) > 16:
            teks = teks[:16]
        self.label_layar.config(text=teks)

    def input_keyboard(self, event):
        char = event.char
        key = event.keysym

        if char in "0123456789.+-()%":
            self.tekan_tombol(char)
        elif char == "*":
            self.tekan_tombol("×")
        elif char == "/":
            self.tekan_tombol("÷")
        elif key in ["Return", "KP_Enter"]:
            self.tekan_tombol("=")
        elif key == "BackSpace":
            self.tekan_tombol("⌫")
        elif key == "Escape":
            self.tekan_tombol("C")


if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorDesktopModern(root)
    root.mainloop()