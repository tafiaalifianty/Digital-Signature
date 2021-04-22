from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile
from pathlib import Path
from RSA import *
from utils import *
from SHA1 import *
import re

class App(Tk):
    def __init__(self):
        super(App, self).__init__()

        self.title("Digital Signature")
        self.resizable(False, False)
        self.minsize(600,300)

        tabControl = ttk.Notebook(self)

        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text = "Pembangkitan Kunci")

        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text = "Pembangkitkan tanda tangan")

        self.tab3 = ttk.Frame(tabControl)
        tabControl.add(self.tab3, text = "Verifikasi tanda tangan")

        tabControl.pack(expand = 1, fill = "both")

        self.render_tab1()
        self.render_tab2()
        self.render_tab3()

    def render_tab1(self):
        key_size_options = [4, 8, 16, 32, 64]
        self.tab1_state = {}
        self.tab1_state['key_size'] = IntVar()
        self.tab1_state['key_size'].set(key_size_options[0])
        self.tab1_state['e'] = StringVar()
        self.tab1_state['d'] = StringVar()
        self.tab1_state['n'] = StringVar()

        labelFrame = LabelFrame(self.tab1, text = "Panjang Kunci")
        labelFrame.grid(column = 0, row = 0, padx = 8)
        for (i, option) in enumerate(key_size_options):
            Radiobutton(labelFrame, text=(str(option)+' bit'), variable=self.tab1_state['key_size'], value=option, width=25, height=2, anchor='w').pack()
        
        Button(master=self.tab1, text="Bangkitkan kunci baru", width=28, command=self.generate_new_key).grid(column=0, row=1, padx=8, pady=4)

        keyFrame = Frame(master=self.tab1)
        keyFrame.grid(column = 1, row = 0, padx = 8, pady = 4)
        publicLabelFrame = LabelFrame(keyFrame, text="Kunci publik")
        publicLabelFrame.grid(column=0, row=0, padx=8, pady=2)
        Label(publicLabelFrame, text="e").grid(column=0, row=0, padx=8, pady=4)
        Entry(publicLabelFrame, textvariable=self.tab1_state['e'], width=50, state=DISABLED, disabledbackground='white').grid(column=1, row=0, padx=8, pady=4)
        Label(publicLabelFrame, text="n").grid(column=0, row=1, padx=8, pady=4)
        Entry(publicLabelFrame, textvariable=self.tab1_state['n'], width=50, state=DISABLED, disabledbackground='white').grid(column=1, row=1, padx=8, pady=4)

        publicLabelFrame = LabelFrame(keyFrame, text="Kunci privat")
        publicLabelFrame.grid(column=0, row=1, padx=8, pady=2)
        Label(publicLabelFrame, text="d").grid(column=0, row=0, padx=8, pady=4)
        Entry(publicLabelFrame, textvariable=self.tab1_state['d'], width=50, state=DISABLED, disabledbackground='white').grid(column=1, row=0, padx=8, pady=4)
        Label(publicLabelFrame, text="n").grid(column=0, row=1, padx=8, pady=4)
        Entry(publicLabelFrame, textvariable=self.tab1_state['n'], width=50, state=DISABLED, disabledbackground='white').grid(column=1, row=1, padx=8, pady=4)

        Button(master=keyFrame, text="Unduh kunci publik", width=49, command=self.download_public_key).grid(column=0, row=2, padx=8, pady=2)
        Button(master=keyFrame, text="Unduh kunci privat", width=49, command=self.download_private_key).grid(column=0, row=3, padx=8, pady=2)
        
    def render_tab2(self):
        self.tab2_state = {}
        self.tab2_state['filename'] = StringVar()
        self.tab2_state['filetype'] = StringVar()
        self.tab2_state['keytype'] = IntVar()
        self.tab2_state['d'] = StringVar()
        self.tab2_state['n'] = StringVar()
        self.tab2_state['file'] = None
        self.tab2_state['file2'] = None
        self.tab2_state['key'] = None

        frame1 = Frame(master=self.tab2)
        frame1.grid(column = 0, row = 0, padx = 8, pady = 4)
        labelFrame = LabelFrame(frame1, text="Sumber berkas")
        labelFrame.grid(column=0, row=0, padx=8, pady=2)

        frame2 = Frame(master=self.tab2)
        frame2.grid(column = 1, row = 0, padx = 8, pady = 4)
        labelFrame2 = LabelFrame(frame2, text="Kunci privat penanda tangan")
        labelFrame2.grid(column=0, row=0, padx=8, pady=2)

        self.tab2_state['filename'].set('Nama berkas: ')
        self.tab2_state['filetype'].set('Format berkas: ')
        Label(labelFrame, textvariable=self.tab2_state['filename'], anchor='w', width=50).grid(column=0, row=0, padx=8)
        Label(labelFrame, textvariable=self.tab2_state['filetype'], anchor='w', width=50).grid(column=0, row=1, padx=8, pady=4)
        Button(master=labelFrame, text="Pilih berkas", width=50, command=lambda: self.open_file(1)).grid(column=0, row=2, padx=8, pady=2)

        self.tab2_state['d'].set('Kunci (d): ')
        self.tab2_state['n'].set('Kunci (n): ')
        Label(labelFrame2, textvariable=self.tab2_state['d'], anchor='w', width=50).grid(column=0, row=0, padx=8, pady=0)
        Label(labelFrame2, textvariable=self.tab2_state['n'], anchor='w', width=50).grid(column=0, row=1, padx=8, pady=4)
        Button(master=labelFrame2, text="Pilih berkas", width=50, command=lambda: self.open_file(2)).grid(column=0, row=2, padx=8, pady=4)
        
        Button(master=frame1, text="Bubuhi tanda tangan langsung", command=lambda: self.signing(1)).grid(column=0, row=1, padx=8, pady=8)
        Button(master=frame2, text="Bubuhi tanda tangan terpisah", command=lambda: self.signing(2)).grid(column=0, row=1, padx=8, pady=8)


    def render_tab3(self):
        self.tab3_state = {}
        self.tab3_state['filename'] = StringVar()
        self.tab3_state['filename2'] = StringVar()
        self.tab3_state['sign2'] = StringVar()
        self.tab3_state['e'] = StringVar()
        self.tab3_state['n'] = StringVar()
        self.tab3_state['key'] = None
        self.tab3_state['file'] = None
        self.tab3_state['file2'] = None

        frame1 = Frame(master=self.tab3)
        frame1.grid(column = 0, row = 0, padx = 8, pady = 4)
        labelFrame = LabelFrame(frame1, text="Tanda tangan langsung")
        labelFrame.grid(column=0, row=0, padx=8, pady=2)
        labelFrame2 = LabelFrame(frame1, text="Tanda tangan terpisah")
        labelFrame2.grid(column=0, row=1, padx=8, pady=2)

        frame2 = Frame(master=self.tab3)
        frame2.grid(column = 1, row = 0, padx = 8, pady = 4)
        labelFrame3 = LabelFrame(frame2, text="Kunci publik penanda tangan")
        labelFrame3.grid(column=0, row=0, padx=8, pady=2)

        self.tab3_state['e'].set('Kunci (e): ')
        self.tab3_state['n'].set('Kunci (n): ')
        Label(labelFrame3, textvariable=self.tab3_state['e'], anchor='w', width=50).grid(column=0, row=0, padx=8, pady=0)
        Label(labelFrame3, textvariable=self.tab3_state['n'], anchor='w', width=50).grid(column=0, row=1, padx=8, pady=4)
        Button(master=labelFrame3, text="Pilih berkas", width=50, command=lambda: self.open_file(3)).grid(column=0, row=2, padx=8, pady=4)

        self.tab3_state['filename'].set('Nama berkas: ')
        Label(labelFrame, textvariable=self.tab3_state['filename'], anchor='w', width=50).grid(column=0, row=0, padx=8)
        Button(master=labelFrame, text="Pilih berkas", width=50, command=lambda: self.open_file(6)).grid(column=0, row=1, padx=8, pady=2)
        Button(master=labelFrame, text="Verifikasi", width=50, command=lambda: self.verify(1)).grid(column=0, row=2, padx=8, pady=10)

        self.tab3_state['filename2'].set('Nama berkas sumber: ')
        Label(labelFrame2, textvariable=self.tab3_state['filename2'], anchor='w', width=50).grid(column=0, row=0, padx=8)
        Button(master=labelFrame2, text="Pilih berkas sumber", width=50, command=lambda: self.open_file(4)).grid(column=0, row=1, padx=8, pady=2)
        self.tab3_state['sign2'].set('')
        Label(labelFrame2, textvariable=self.tab3_state['sign2'], anchor='w', width=50).grid(column=0, row=2, padx=8)
        Button(master=labelFrame2, text="Pilih berkas tanda tangan", width=50, command=lambda: self.open_file(5)).grid(column=0, row=3, padx=8, pady=2)
        Button(master=labelFrame2, text="Verifikasi", width=50, command=lambda: self.verify(2)).grid(column=0, row=4, padx=8, pady=10)

    def generate_new_key(self):
        d, e, n = generate_key(self.tab1_state['key_size'].get())

        self.tab1_state['d'].set(d)
        self.tab1_state['e'].set(e)
        self.tab1_state['n'].set(n)

    def download_public_key(self):
        e = self.tab1_state['e'].get()
        n = self.tab1_state['n'].get()
        if(e == '' or n == ''):
            messagebox.showerror('Gagal!', 'Lakukan pembangkitan kunci terlebih dahulu!')
        else:
            try:
                f = asksaveasfile(mode='w', defaultextension='.pub')
                if(f is None):
                    return
                f.write("<" + e + "," + n + ">")
                f.close
            except Exception as err:
                messagebox.showerror('Gagal!', err)
    
    def download_file(self, message):
        if(message == None):
            messagebox.showerror('Gagal!', 'Kesalahan pesan')
        else:
            try:
                f = asksaveasfile(mode='w')
                if(f is None):
                    return
                f.write(message)
                f.close
            except Exception as err:
                messagebox.showerror('Gagal!', err)
    
    def download_private_key(self):
        d = self.tab1_state['d'].get()
        n = self.tab1_state['n'].get()
        if(d == '' or n == ''):
            messagebox.showerror('Gagal!', 'Lakukan pembangkitan kunci terlebih dahulu!')
        else:
            try:
                f = asksaveasfile(mode='w', defaultextension='.pri')
                if(f is None):
                    return
                f.write("<" + d + "," + n + ">")
                f.close
            except Exception as e:
                messagebox.showerror('Gagal!', e)
    
    def open_file(self, mode):
        try:
            file = askopenfile(mode='r', title='Pilih berkas')
            if file is not None:
                if(mode == 1):
                    self.tab2_state['filename'].set('Nama berkas: ' + str(Path(file.name).name))
                    self.tab2_state['filetype'].set('Format berkas: ' + str(Path(file.name).name.split('.')[-1].upper()))
                    self.tab2_state['file'] = file
                elif(mode == 2 or mode == 3):
                    content = file.read()
                    content = content.replace('<', '')
                    content = content.replace('>', '')
                    content = content.split(',')
                    if(len(content) != 2):
                        messagebox.showerror('Gagal!', 'Pilih kembali berkas!')
                    else:
                        if(mode == 2):
                            self.tab2_state['key'] = file
                            self.tab2_state['d'].set('Kunci (d): ' + str(content[0]))
                            self.tab2_state['n'].set('Kunci (n): ' + str(content[1]))
                        else:
                            self.tab3_state['key'] = file
                            self.tab3_state['e'].set('Kunci (e): ' + str(content[0]))
                            self.tab3_state['n'].set('Kunci (n): ' + str(content[1]))
                elif(mode == 4):
                    self.tab3_state['filename2'].set('Nama berkas sumber: ' + str(Path(file.name).name))
                    self.tab3_state['file2'] = file
                elif(mode == 6):
                    self.tab3_state['filename'].set('Nama berkas sumber: ' + str(Path(file.name).name))
                    self.tab3_state['file'] = file
                elif(mode == 5):
                    content = file.read()
                    if('<DIGITALSIGNATURE>' in content and '</DIGITALSIGNATURE>' in content):
                        content = content.replace('<DIGITALSIGNATURE>', '')
                        content = content.replace('</DIGITALSIGNATURE>', '')
                        content = content.split('\n')
                        if(content == '' or len(content) > 1):
                            messagebox.showerror('Gagal!', 'Pilih kembali berkas!')
                        else:
                            self.tab3_state['sign2'].set(content[0])
                    else:
                        messagebox.showerror('Gagal!', 'Pilih kembali berkas!')  
        except Exception as e:
            messagebox.showerror('Gagal!', 'Pilih kembali berkas!')

    def check_read_file(self):
        try:
            f = open(Path(self.tab2_state['file'].name), 'r')
            f.read()
            f.close()
        except:
            raise Exception('Berkas tidak kompatibel untuk dibubuhi tanda tangan langsung!')

    def signing(self, mode):
        try:
            if(self.tab2_state['file'] == None or self.tab2_state['key'] == None):
                # messagebox.showerror('Gagal!', 'Pilih berkas dan kunci terlebih dahulu!')
                raise Exception('Pilih berkas dan kunci terlebih dahulu!')
            if(mode == 1):
                d = int(self.tab2_state['d'].get().replace('Kunci (d): ', ''))
                n = int(self.tab2_state['n'].get().replace('Kunci (n): ', ''))
                self.check_read_file()
                with open(Path(self.tab2_state['file'].name), 'r+') as f :
                    content = f.read()
                    hex_digest = text_hash(content)
                    sign = encrypt((d, n), hex_digest)
                    sign = '\n<DIGITALSIGNATURE>' + sign + '</DIGITALSIGNATURE>'
                    f.write(sign)

                    f.close()
            elif(mode == 2):
                d = int(self.tab2_state['d'].get().replace('Kunci (d): ', ''))
                n = int(self.tab2_state['n'].get().replace('Kunci (n): ', ''))
                hex_digest = file_hash(Path(self.tab2_state['file'].name))
                sign = encrypt((d, n), hex_digest)
                sign = '<DIGITALSIGNATURE>' + sign + '</DIGITALSIGNATURE>'
                self.download_file(sign)
            messagebox.showinfo('Sukses', 'Berhasil membubuhi tanda tangan')

        except Exception as e:
            messagebox.showerror('Gagal!', e)

    def verify(self, mode):
        try:
            if(mode == 2):
                if(self.tab3_state['key'] == None or self.tab3_state['file2'] == None or self.tab3_state['sign2'].get() == ''):
                    raise Exception('Pilih berkas dan kunci terlebih dahulu!')
                else:
                    print(self.tab3_state['sign2'].get())
                    e = int(self.tab3_state['e'].get().replace('Kunci (e): ', ''))
                    n = int(self.tab3_state['n'].get().replace('Kunci (n): ', ''))
                    digital_signature_plain = decrypt((e, n), self.tab3_state['sign2'].get())
                    hex_digest = file_hash(Path(self.tab3_state['file2'].name))
                    if(digital_signature_plain == hex_digest):
                        messagebox.showinfo('Sukses!', 'Terverifikasi!')
                    else:
                        messagebox.showerror('Gagal!', 'Tidak terverifikasi!')
            else:
                if(self.tab3_state['key'] == None or self.tab3_state['file'] == None):
                    raise Exception('Pilih berkas dan kunci terlebih dahulu!')
                else:
                    with open(Path(self.tab3_state['file'].name), 'r') as f :
                        content = f.read()
                        sign = re.findall(r"<DIGITALSIGNATURE>(.*)<\/DIGITALSIGNATURE>", content)
                        if(len(sign)):
                            e = int(self.tab3_state['e'].get().replace('Kunci (e): ', ''))
                            n = int(self.tab3_state['n'].get().replace('Kunci (n): ', ''))
                            cipher_sign = sign[-1]
                            message = content.replace(("\n<DIGITALSIGNATURE>"+str(cipher_sign)+"</DIGITALSIGNATURE>"), '')
                            hex_digest = text_hash(message)
                            digital_signature_plain = decrypt((e,n), str(cipher_sign))

                            if(digital_signature_plain == hex_digest):
                                messagebox.showinfo('Sukses!', 'Terverifikasi!')
                            else:
                                messagebox.showerror('Gagal!', 'Tidak terverifikasi!')

                        else:
                            raise Exception('Berkas tidak mengandung tanda tangan')
        except Exception as e:
            messagebox.showerror('Gagal!', e)

if __name__ == '__main__':
    app = App()
    app.mainloop()