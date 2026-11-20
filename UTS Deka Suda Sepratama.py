"""
PROJECT SISTEM INVENTARIS
Mata Kuliah: Pemrograman Berorientasi Objek
Bahasa: Python 3

Fitur:
- Menambah, menampilkan, mencari, mengubah, dan menghapus barang
- Menambah dan mengurangi stok
- Menampilkan ringkasan inventaris

Konsep OOP yang diterapkan:
- Class dan object: class Barang dan Inventaris
- Constructor: __init__()
- Attribute dan method
- Encapsulation: attribute _stok dan __barang
- Property/setter: property stok pada class Barang
- Class method: Barang.dari_input()
- Static method: Barang.validasi_nama()
"""

class Barang:
    """Mewakili satu barang dalam inventaris."""

    jumlah_barang_dibuat = 0  # attribute milik class

    def __init__(self, kode, nama, kategori, stok, harga):
        self.kode = str(kode).strip().upper()
        self.nama = str(nama).strip()
        self.kategori = str(kategori).strip()
        self._stok = 0
        self.stok = stok             # menggunakan setter
        self.harga = float(harga)
        Barang.jumlah_barang_dibuat += 1

    @property
    def stok(self):
        """Mengambil nilai stok."""
        return self._stok

    @stok.setter
    def stok(self, nilai):
        """Mengatur stok agar tidak bernilai negatif."""
        nilai = int(nilai)
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif.")
        self._stok = nilai

    @staticmethod
    def validasi_nama(nama):
        """Static method: memeriksa apakah nama barang valid."""
        return bool(str(nama).strip())

    @classmethod
    def dari_input(cls):
        """Class method: membuat object Barang dari input pengguna."""
        print("\n--- Input Barang Baru ---")
        kode = input("Kode barang       : ").strip()
        nama = input("Nama barang       : ").strip()
        if not cls.validasi_nama(nama):
            raise ValueError("Nama barang tidak boleh kosong.")
        kategori = input("Kategori          : ").strip()
        stok = int(input("Stok awal         : "))
        harga = float(input("Harga satuan (Rp) : "))
        return cls(kode, nama, kategori, stok, harga)

    def tambah_stok(self, jumlah):
        jumlah = int(jumlah)
        if jumlah <= 0:
            raise ValueError("Jumlah penambahan harus lebih dari 0.")
        self.stok += jumlah

    def kurangi_stok(self, jumlah):
        jumlah = int(jumlah)
        if jumlah <= 0:
            raise ValueError("Jumlah pengurangan harus lebih dari 0.")
        if jumlah > self.stok:
            raise ValueError("Stok tidak mencukupi.")
        self.stok -= jumlah

    def nilai_persediaan(self):
        return self.stok * self.harga

    def tampilkan(self):
        print(
            f"{self.kode:<10} {self.nama:<20} {self.kategori:<15} "
            f"{self.stok:>6} {self.harga:>14,.2f} "
            f"{self.nilai_persediaan():>18,.2f}"
        )


class Inventaris:
    """Mengelola kumpulan object Barang."""

    def __init__(self, nama_toko):
        self.nama_toko = nama_toko
        self.__barang = {}  # encapsulation: data barang disembunyikan

    def tambah_barang(self, barang):
        if not isinstance(barang, Barang):
            raise TypeError("Data yang ditambahkan harus berupa object Barang.")
        if barang.kode in self.__barang:
            raise ValueError("Kode barang sudah digunakan.")
        self.__barang[barang.kode] = barang

    def tampilkan_semua(self):
        if not self.__barang:
            print("\nInventaris masih kosong.")
            return
        self._tampilkan_header()
        for barang in self.__barang.values():
            barang.tampilkan()

    @staticmethod
    def _tampilkan_header():
        print("\n" + "=" * 105)
        print(f"{'KODE':<10} {'NAMA BARANG':<20} {'KATEGORI':<15} "
              f"{'STOK':>6} {'HARGA (Rp)':>14} {'NILAI STOK (Rp)':>18}")
        print("-" * 105)

    def cari_barang(self, kata_kunci):
        kata_kunci = kata_kunci.strip().lower()
        hasil = [
            barang for barang in self.__barang.values()
            if kata_kunci in barang.kode.lower()
            or kata_kunci in barang.nama.lower()
            or kata_kunci in barang.kategori.lower()
        ]
        if not hasil:
            print("Barang tidak ditemukan.")
            return
        self._tampilkan_header()
        for barang in hasil:
            barang.tampilkan()

    def ambil_barang(self, kode):
        kode = kode.strip().upper()
        if kode not in self.__barang:
            raise KeyError("Kode barang tidak ditemukan.")
        return self.__barang[kode]

    def ubah_barang(self, kode, nama_baru, kategori_baru, harga_baru):
        barang = self.ambil_barang(kode)
        if not Barang.validasi_nama(nama_baru):
            raise ValueError("Nama barang tidak boleh kosong.")
        barang.nama = nama_baru.strip()
        barang.kategori = kategori_baru.strip()
        barang.harga = float(harga_baru)
        if barang.harga < 0:
            raise ValueError("Harga tidak boleh negatif.")

    def hapus_barang(self, kode):
        kode = kode.strip().upper()
        if kode not in self.__barang:
            raise KeyError("Kode barang tidak ditemukan.")
        del self.__barang[kode]

    def ringkasan(self):
        total_jenis = len(self.__barang)
        total_unit = sum(b.stok for b in self.__barang.values())
        total_nilai = sum(b.nilai_persediaan() for b in self.__barang.values())
        print("\n========== RINGKASAN INVENTARIS ==========")
        print(f"Nama toko             : {self.nama_toko}")
        print(f"Jumlah jenis barang   : {total_jenis}")
        print(f"Total seluruh stok   : {total_unit} unit")
        print(f"Total nilai persediaan: Rp {total_nilai:,.2f}")
        print("==========================================")


def tampilkan_menu():
    print("""
============= SISTEM INVENTARIS =============
1. Tambah barang
2. Tampilkan semua barang
3. Cari barang
4. Tambah stok
5. Kurangi stok
6. Ubah data barang
7. Hapus barang
8. Ringkasan inventaris
0. Keluar
=============================================
""")


def jalankan_program():
    print("SELAMAT DATANG DI SISTEM INVENTARIS")
    nama_toko = input("Masukkan nama toko/gudang: ").strip() or "Gudang Utama"
    inventaris = Inventaris(nama_toko)

    # Contoh object awal agar program langsung bisa dicoba.
    inventaris.tambah_barang(Barang("BRG001", "Buku Tulis", "Alat Tulis", 25, 5000))
    inventaris.tambah_barang(Barang("BRG002", "Pulpen", "Alat Tulis", 40, 3000))
    inventaris.tambah_barang(Barang("BRG003", "Mouse", "Elektronik", 10, 75000))

    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu: ").strip()

        try:
            if pilihan == "1":
                barang = Barang.dari_input()
                inventaris.tambah_barang(barang)
                print("Barang berhasil ditambahkan.")

            elif pilihan == "2":
                inventaris.tampilkan_semua()

            elif pilihan == "3":
                kata = input("Masukkan kode/nama/kategori: ")
                inventaris.cari_barang(kata)

            elif pilihan == "4":
                kode = input("Kode barang: ")
                jumlah = int(input("Jumlah stok yang ditambahkan: "))
                inventaris.ambil_barang(kode).tambah_stok(jumlah)
                print("Stok berhasil ditambahkan.")

            elif pilihan == "5":
                kode = input("Kode barang: ")
                jumlah = int(input("Jumlah stok yang dikeluarkan: "))
                inventaris.ambil_barang(kode).kurangi_stok(jumlah)
                print("Stok berhasil dikurangi.")

            elif pilihan == "6":
                kode = input("Kode barang yang akan diubah: ")
                nama = input("Nama baru: ")
                kategori = input("Kategori baru: ")
                harga = float(input("Harga baru: "))
                inventaris.ubah_barang(kode, nama, kategori, harga)
                print("Data barang berhasil diubah.")

            elif pilihan == "7":
                kode = input("Kode barang yang akan dihapus: ")
                inventaris.hapus_barang(kode)
                print("Barang berhasil dihapus.")

            elif pilihan == "8":
                inventaris.ringkasan()

            elif pilihan == "0":
                print("Terima kasih. Program selesai.")
                break

            else:
                print("Pilihan tidak tersedia. Silakan pilih menu 0-8.")

        except ValueError as error:
            print(f"Input tidak valid: {error}")
        except (KeyError, TypeError) as error:
            print(f"Terjadi kesalahan: {error}")


if __name__ == "__main__":
    jalankan_program()
