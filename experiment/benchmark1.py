import time, random
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

random.seed(99)

TIER = {'PREMIUM': 1, 'REGULAR': 2, 'ECONOMY': 3}

@dataclass
class Produk:
    kode: str                 # P001-P100
    nama: str
    harga: float
    stok: int

@dataclass
class Order:
    order_id: int
    pelanggan: str            # C001-C050
    produk_kode: str
    tier: int                 # 1=PREMIUM, 2=REGULAR, 3=ECONOMY
    qty: int
    total_harga: float
    waktu_pesan: float        # time.time()

# ── Queue berbasis list (dequeue O(n)) ─────────────────────────
class Queue:
    def __init__(self):
        self.data: List[Order] = []

    def enqueue(self, order: Order) -> None:
        self.data.append(order)

    def dequeue(self) -> Optional[Order]:
        if not self.data:
            return None
        return self.data.pop(0)

    def is_empty(self) -> bool:
        return len(self.data) == 0

    def __len__(self) -> int:
        return len(self.data)

# ── Stack berbasis list (pasang & cabut sederhana) ──────────────
class Stack:
    def __init__(self):
        self.data: List[Order] = []

    def push(self, order: Order) -> None:
        self.data.append(order)

    def pop(self) -> Optional[Order]:
        if not self.data:
            return None
        return self.data.pop()

    def top(self) -> Optional[Order]:
        return self.data[-1] if self.data else None

    def __len__(self) -> int:
        return len(self.data)

# ── Katalog produk berbasis list (linear search) ───────────────
class Katalog:
    def __init__(self):
        self.produks: List[Produk] = []

    def insert(self, produk: Produk) -> None:
        self.produks.append(produk)

    def search(self, kode: str) -> Optional[Produk]:
        for prod in self.produks:
            if prod.kode == kode:
                return prod
        return None

    def update_stok(self, kode: str, qty_delta: int) -> bool:
        prod = self.search(kode)
        if prod:
            prod.stok += qty_delta
            return True
        return False

    def all_produk(self) -> List[Produk]:
        return list(self.produks)

# ── Graph rekomendasi sederhana, tidak dioptimalkan ─────────────
class GraphRekomendasi:
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, int]]] = {}

    def add_copurchase(self, kode_a: str, kode_b: str) -> None:
        if kode_a not in self.adj:
            self.adj[kode_a] = []
        for i, (kode, freq) in enumerate(self.adj[kode_a]):
            if kode == kode_b:
                self.adj[kode_a][i] = (kode, freq + 1)
                return
        self.adj[kode_a].append((kode_b, 1))

    def rekomendasi(self, kode_produk: str, max_hop: int = 2) -> List[str]:
        if kode_produk not in self.adj:
            return []
        rekomendasi_list: List[str] = []
        current_layer = [kode_produk]
        visited = [kode_produk]
        hop = 0
        while hop < max_hop and current_layer:
            next_layer: List[str] = []
            for kode in current_layer:
                for neighbor, _ in self.adj.get(kode, []):
                    if neighbor not in visited:
                        visited.append(neighbor)
                        rekomendasi_list.append(neighbor)
                        next_layer.append(neighbor)
            current_layer = next_layer
            hop += 1
        return rekomendasi_list

# ── Generator data awal ──────────────────────────────────────

def generate_produk(n=100) -> List[Produk]:
    nama_template = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headset',
                     'Webcam', 'USB Hub', 'Charger', 'Kabel HDMI', 'Speaker']

    produk_list = []
    for i in range(1, n + 1):
        kode = f'P{i:03d}'
        nama = f"{random.choice(nama_template)} Model-{i}"
        harga = round(random.uniform(50_000, 5_000_000), -3)
        stok = random.randint(0, 200)
        produk_list.append(Produk(kode, nama, harga, stok))
    return produk_list

# ── Sorting laporan harian (masih O(n²)) ──────────────────────

def bubble_sort_by_harga(orders: List[Order]) -> List[Order]:
    arr = orders.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j].total_harga < arr[j + 1].total_harga:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort_by_waktu(orders: List[Order]) -> List[Order]:
    arr = orders.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j].waktu_pesan > key.waktu_pesan:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def tambah_order(pelanggan: str, produk: str, tier_str: str,
                 katalog: Katalog, queues: Dict[str, Queue],
                 riwayat: Dict[str, List[Order]], order_counter: int) -> tuple[int, bool, str]:
    if tier_str not in TIER:
        return order_counter, False, f"✗ Tier '{tier_str}' tidak valid. Gunakan: PREMIUM, REGULAR, ECONOMY"

    prod = katalog.search(produk)
    if not prod:
        return order_counter, False, f"✗ Produk {produk} tidak ditemukan"

    if prod.stok <= 0:
        return order_counter, False, f"✗ Produk {produk} stok habis"

    order_counter += 1
    order = Order(order_counter, pelanggan, produk, TIER[tier_str], 1, prod.harga, time.time())
    queues[tier_str].enqueue(order)

    if pelanggan not in riwayat:
        riwayat[pelanggan] = []
    riwayat[pelanggan].append(order)

    prod.stok -= 1
    return order_counter, True, f"✓ Order {order_counter}: {pelanggan} - {produk} ({tier_str}) - Rp {prod.harga:,.0f}"


def main():
    queues = {tier: Queue() for tier in TIER}
    riwayat: Dict[str, List[Order]] = {}
    katalog = Katalog()
    graph_rek = GraphRekomendasi()
    completed_orders: List[Order] = []
    order_counter = 0

    for p in generate_produk(100):
        katalog.insert(p)

    print("=" * 70)
    print("E-Commerce Order Management & Recommendation Engine (Naive)".center(70))
    print("=" * 70)
    print("Ketik BANTUAN untuk daftar perintah\n")

    while True:
        try:
            cmd = input("> ").strip()
            if not cmd:
                continue
            parts = cmd.split()
            perintah = parts[0].upper()

            if perintah == "BANTUAN":
                print("\n" + "="*70)
                print("DAFTAR PERINTAH".ljust(70))
                print("="*70)
                print("  ORDER <cust> <prod> <tier>     - Tambah order")
                print("  BATCH_ORDER <jumlah>           - Tambah banyak order sekaligus")
                print("  SERVE                          - Layani order PREMIUM→REGULAR→ECONOMY")
                print("  CANCEL_LAST                    - Batalkan order terakhir")
                print("  CARI_PRODUK <kode>             - Cari produk")
                print("  UPDATE_STOK <kode> <qty>       - Update stok")
                print("  REKOMENDASI <kode_produk>      - Rekomendasi produk")
                print("  RIWAYAT <cust>                 - Riwayat order pelanggan")
                print("  LAPORAN_HARIAN                 - Laporan order")
                print("  KELUAR                         - Keluar program")
                print("="*70 + "\n")

            elif perintah == "ORDER" and len(parts) >= 4:
                pelanggan, produk, tier_str = parts[1], parts[2], parts[3].upper()
                order_counter, success, msg = tambah_order(pelanggan, produk, tier_str,
                                                          katalog, queues, riwayat, order_counter)
                print(f"  {msg}\n")

            elif perintah == "BATCH_ORDER" and len(parts) >= 2:
                try:
                    batch_count = int(parts[1])
                except ValueError:
                    print("  ✗ Jumlah batch harus berupa angka\n")
                    continue
                print(f"  Masukkan {batch_count} baris order. Format tiap baris: C001 P001 PREMIUM")
                loaded = 0
                while loaded < batch_count:
                    line = input().strip()
                    if not line:
                        continue
                    row = line.split()
                    if row[0].upper() == "ORDER":
                        row = row[1:]
                    if len(row) != 3:
                        print(f"  ✗ Baris {loaded + 1} salah: {line}")
                        loaded += 1
                        continue
                    pelanggan, produk, tier_str = row[0], row[1], row[2].upper()
                    order_counter, success, msg = tambah_order(pelanggan, produk, tier_str,
                                                              katalog, queues, riwayat, order_counter)
                    print(f"  {msg}")
                    loaded += 1
                print(f"  Selesai memproses {batch_count} order.\n")

            elif perintah == "SERVE":
                served = False
                for tier_name in ['PREMIUM', 'REGULAR', 'ECONOMY']:
                    if not queues[tier_name].is_empty():
                        order = queues[tier_name].dequeue()
                        if order:
                            completed_orders.append(order)
                            graph_rek.add_copurchase(order.produk_kode, order.produk_kode)
                            print(f"  ✓ SERVE Order {order.order_id}: {order.pelanggan} - {order.produk_kode} ({tier_name})")
                            print(f"  [Dequeue O(n) karena pop(0) pada list]\n")
                            served = True
                            break
                if not served:
                    print("  ✗ Tidak ada order dalam antrian\n")

            elif perintah == "CANCEL_LAST":
                cancelled = False
                for pelanggan, orders in riwayat.items():
                    if orders:
                        last_order = orders.pop()
                        print(f"  ✓ CANCEL Order {last_order.order_id}: {pelanggan} - {last_order.produk_kode}")
                        cancelled = True
                        break
                if not cancelled:
                    print("  ✗ Tidak ada order untuk dibatalkan\n")

            elif perintah == "CARI_PRODUK" and len(parts) >= 2:
                kode = parts[1].upper()
                produk = katalog.search(kode)
                if produk:
                    print(f"\n  Kode  : {produk.kode}")
                    print(f"  Nama  : {produk.nama}")
                    print(f"  Harga : Rp {produk.harga:,.0f}")
                    print(f"  Stok  : {produk.stok}")
                    print(f"  [Search O(n): linear scan list]\n")
                else:
                    print(f"  ✗ Produk {kode} tidak ditemukan\n")

            elif perintah == "UPDATE_STOK" and len(parts) >= 3:
                kode = parts[1].upper()
                try:
                    qty = int(parts[2])
                    if katalog.update_stok(kode, qty):
                        prod = katalog.search(kode)
                        print(f"  ✓ UPDATE STOK {kode}: {qty:+d} → Stok baru: {prod.stok}")
                        print(f"  [Search O(n) + update O(1)]\n")
                    else:
                        print(f"  ✗ Produk {kode} tidak ditemukan\n")
                except ValueError:
                    print(f"  ✗ Qty harus berupa angka\n")

            elif perintah == "REKOMENDASI" and len(parts) >= 2:
                kode = parts[1].upper()
                recom = graph_rek.rekomendasi(kode, max_hop=2)
                if recom:
                    print(f"  Rekomendasi untuk {kode}: {', '.join(recom)}")
                    print(f"  [Rekomendasi berbasis BFS sederhana]\n")
                else:
                    print(f"  Tidak ada rekomendasi untuk {kode}\n")

            elif perintah == "RIWAYAT" and len(parts) >= 2:
                pelanggan = parts[1]
                if pelanggan in riwayat and riwayat[pelanggan]:
                    print(f"\n  Riwayat Order {pelanggan}:")
                    for i, order in enumerate(reversed(riwayat[pelanggan]), 1):
                        if i > 10:
                            break
                        print(f"    {i}. Order {order.order_id} - {order.produk_kode} - Rp {order.total_harga:,.0f}")
                    print(f"  [Traversal O(n) karena list terbalik]\n")
                else:
                    print(f"  ✗ Pelanggan {pelanggan} tidak ditemukan atau belum punya order\n")

            elif perintah == "LAPORAN_HARIAN":
                if not completed_orders:
                    print("  ✗ Tidak ada order yang selesai\n")
                    continue
                print(f"\n  {'='*68}")
                print(f"  LAPORAN HARIAN - Total Order: {len(completed_orders)}".center(68))
                print(f"  {'='*68}")

                print(f"\n  [1] Sorted by Harga (Descending) - Bubble Sort O(n²):")
                bubble_sorted = bubble_sort_by_harga(completed_orders)
                for i, order in enumerate(bubble_sorted[:5], 1):
                    print(f"      {i}. Order {order.order_id} - {order.produk_kode} - Rp {order.total_harga:,.0f}")

                print(f"\n  [2] Sorted by Waktu (Ascending) - Insertion Sort O(n²):")
                insertion_sorted = insertion_sort_by_waktu(completed_orders)
                for i, order in enumerate(insertion_sorted[:5], 1):
                    waktu = time.strftime("%H:%M:%S", time.localtime(order.waktu_pesan))
                    print(f"      {i}. Order {order.order_id} - {waktu}")

                print(f"  {'='*68}\n")

            elif perintah == "KELUAR":
                print("  Terima kasih! Sampai jumpa.\n")
                break

            else:
                print(f"  ✗ Perintah '{perintah}' tidak dikenali. Ketik BANTUAN\n")

        except KeyboardInterrupt:
            print("\n  Program dihentikan.\n")
            break
        except Exception as e:
            print(f"  ✗ Error: {e}\n")

if __name__ == "__main__":
    main()
CODE BANDING
