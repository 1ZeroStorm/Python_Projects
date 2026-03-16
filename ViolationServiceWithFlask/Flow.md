

```mermaid
flowchart TD

subgraph Flow_Besar_Sistem [Flow Besar Sistem]
    A[User Browser] --> B[Halaman HTML]
    B --> C[Routing Flask]
    C --> D[Proses Backend, contoh: view, ambil data]
    D --> E[Database MySQL, mengembalikan data]
    E --> F[Response ke User, menunjukkan data ke user]
end
```
## Jelaskan secara singkat bagaimana request diproses dari user sampai kembali ke halaman.

---
# FLOW CRUD

```mermaid
flowchart TD
subgraph Flow_Create [Flow Create]
    C1[User isi data] --> C2[Submit]
    C2 --> C3[Routing menerima POST]
    C3 --> C4[Simpan ke database]
    C4 --> C5[Redirect ke halaman list]
end
```
---
```mermaid
flowchart TD
subgraph Flow_Read [Flow Read]
    R1[User mentrigger UI] --> R2[Routing dipanggil]
    R2 --> R3[Ambil data dari database]
    R3 --> R4[Tampilkan di tabel HTML]
end

```
---
```mermaid
flowchart TD
    U1[User klik edit] --> U2[Ubah data]
    U2 --> U3[Database diperbarui]

    D1[User klik delete] --> D2[Routing menerima ID]
    D2 --> D3[Data dihapus dari database]
```
---
```mermaid
flowchart TD
    X1[User klik export] --> X2[Routing export dipanggil]
    X2 --> X3[Ambil semua data]
    X3 --> X4[Bentuk file CSV]
    X4 --> X5[File diunduh]
```
---
```mermaid
flowchart TD
    I1[User upload file CSV] --> I2[Routing menerima file]
    I2 --> I3[Backend membaca file]
    I3 --> I4[Data dimasukkan ke database]
    I4 --> I5[Redirect dengan pesan hasil]
```

## Jelaskan bahwa sistem harus menangani error agar tidak crash jika data tidak valid. (contoh import)
```mermaid
flowchart TD
    I1[User upload file CSV] --> I2[Routing menerima file, exeption handling]
    I2 --> I3[Backend membaca file]
    I3 --> I4[Data dimasukkan ke database]
    I4 --> I5[Redirect dengan pesan hasil]
```
---


