import time, random
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple

random.seed(99)

TIER = {'PREMIUM': 1, 'REGULAR': 2, 'ECONOMY': 3}
TIER_NAME = {v: k for k, v in TIER.items()}

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

# ── Node Linked List ─────────────────────────────────────────
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None

# ── Queue berbasis Linked List ───────────────────────────────
class Queue:
    """FIFO Queue berbasis Singly Linked List."""
    def __init__(self):
        self.head: Optional[LLNode] = None
        self.tail: Optional[LLNode] = None
        self._size: int = 0

    def enqueue(self, data) -> None:
        new_node = LLNode(data)
        if self.is_empty():
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        if self.is_empty():
            self.tail = None
        return data

    def peek(self):
        return self.head.data if self.head else None

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def remove_by_condition(self, predicate) -> bool:
        prev = None
        current = self.head
        while current:
            if predicate(current.data):
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                if current is self.tail:
                    self.tail = prev
                self._size -= 1
                return True
            prev = current
            current = current.next
        return False

# ── Stack berbasis Linked List ───────────────────────────────
class Stack:
    def __init__(self, kapasitas=10):
        self.top: Optional[LLNode] = None
        self._size: int = 0
        self.kapasitas = kapasitas

    def push(self, data) -> bool:
        if self._size >= self.kapasitas:
            return False
        new_node = LLNode(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1
        return True

    def pop(self):
        if self.top is None:
            return None
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data

    def remove_by_condition(self, predicate) -> bool:
        prev = None
        current = self.top
        while current:
            if predicate(current.data):
                if prev:
                    prev.next = current.next
                else:
                    self.top = current.next
                self._size -= 1
                return True
            prev = current
            current = current.next
        return False

# ── BST Katalog Produk (implementasikan) ─────────────────────
class BSTNode:
    def __init__(self, produk: Produk):
        self.produk = produk
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BSTKatalog:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, produk: Produk) -> None:
        if self.root is None:
            self.root = BSTNode(produk)
        else:
            self._insert_recursive(self.root, produk)
    
    def _insert_recursive(self, node: BSTNode, produk: Produk) -> None:
        if produk.kode < node.produk.kode:
            if node.left is None:
                node.left = BSTNode(produk)
            else:
                self._insert_recursive(node.left, produk)
        else:
            if node.right is None:
                node.right = BSTNode(produk)
            else:
                self._insert_recursive(node.right, produk)

    def search(self, kode: str) -> Optional[Produk]:
        return self._search_recursive(self.root, kode)
    
    def _search_recursive(self, node: Optional[BSTNode], kode: str) -> Optional[Produk]:
        if node is None:
            return None
        if kode == node.produk.kode:
            return node.produk
        elif kode < node.produk.kode:
            return self._search_recursive(node.left, kode)
        else:
            return self._search_recursive(node.right, kode)

    def update_stok(self, kode: str, qty_delta: int) -> bool:
        return self._update_stok_recursive(self.root, kode, qty_delta)
    
    def _update_stok_recursive(self, node: Optional[BSTNode], kode: str, qty_delta: int) -> bool:
        if node is None:
            return False
        if kode == node.produk.kode:
            node.produk.stok += qty_delta
            return True
        elif kode < node.produk.kode:
            return self._update_stok_recursive(node.left, kode, qty_delta)
        else:
            return self._update_stok_recursive(node.right, kode, qty_delta)

    def inorder(self) -> List[Produk]:
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[BSTNode], result: List[Produk]) -> None:
        if node is None:
            return
        self._inorder_recursive(node.left, result)
        result.append(node.produk)
        self._inorder_recursive(node.right, result)

# ── Graph Rekomendasi (implementasikan) ──────────────────────
class GraphRekomendasi:
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, int]]] = {}  # kode -> [(kode, freq)]

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
        visited = set()
        rekomendasi_list = []
        q = Queue()
        q.enqueue((kode_produk, 0))
        visited.add(kode_produk)
        while not q.is_empty():
            kode, hop = q.dequeue()
            if hop < max_hop and kode in self.adj:
                for neighbor_kode, _ in self.adj[kode]:
                    if neighbor_kode not in visited:
                        visited.add(neighbor_kode)
                        rekomendasi_list.append(neighbor_kode)
                        q.enqueue((neighbor_kode, hop + 1))
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

# ── Sorting Laporan Harian ───────────────────────────────────
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

def main():
    # Inisialisasi
    queues = {tier: Queue() for tier in TIER}
    cust_stacks: Dict[str, Stack] = {}
    bst_katalog = BSTKatalog()
    graph_rek = GraphRekomendasi()
    completed_orders: List[Order] = []
    order_counter = 0
    order_stack = Stack(kapasitas=10000)
    canceled_orders = set()
    customer_history: Dict[str, List[str]] = {}
    last_customer = None  # Track pelanggan terakhir yang order

    for p in generate_produk(100):
        bst_katalog.insert(p)

    print("=" * 70)
    print("E-Commerce Order Management & Recommendation Engine".center(70))
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
                if tier_str not in TIER:
                    print(f"  ✗ Tier '{tier_str}' tidak valid. Gunakan: PREMIUM, REGULAR, ECONOMY\n")
                    continue
                
                prod = bst_katalog.search(produk)
                if not prod:
                    print(f"  ✗ Produk {produk} tidak ditemukan\n")
                    continue
                
                if prod.stok <= 0:
                    print(f"  ✗ Produk {produk} stok habis\n")
                    continue
                
                order_counter += 1
                order = Order(order_counter, pelanggan, produk, TIER[tier_str], 1, prod.harga, time.time())
                queues[tier_str].enqueue(order)
                
                if pelanggan not in cust_stacks:
                    cust_stacks[pelanggan] = Stack(kapasitas=10)
                cust_stacks[pelanggan].push(order)
                order_stack.push(order)
                last_customer = pelanggan  # Update pelanggan terakhir
                
                print(f"  ✓ Order {order_counter}: {pelanggan} - {produk} ({tier_str}) - Rp {prod.harga:,.0f}")
                print(f"  [O(1): Enqueue ke tier queue]\n")

            elif perintah == "SERVE":
                served = False
                for tier_name in ['PREMIUM', 'REGULAR', 'ECONOMY']:
                    while not queues[tier_name].is_empty():
                        order = queues[tier_name].dequeue()
                        if order.order_id in canceled_orders:
                            continue
                        prod = bst_katalog.search(order.produk_kode)
                        if prod and bst_katalog.update_stok(order.produk_kode, -1):
                            order_stack.remove_by_condition(lambda o: o.order_id == order.order_id)
                            completed_orders.append(order)
                            if order.pelanggan not in customer_history:
                                customer_history[order.pelanggan] = []
                            for prev_produk in customer_history[order.pelanggan]:
                                graph_rek.add_copurchase(prev_produk, order.produk_kode)
                                graph_rek.add_copurchase(order.produk_kode, prev_produk)
                            customer_history[order.pelanggan].append(order.produk_kode)
                            print(f"  ✓ SERVE Order {order.order_id}: {order.pelanggan} - {order.produk_kode} ({tier_name})")
                            print(f"  [O(1): Dequeue + O(log n): Update stok BST]\n")
                            served = True
                            break
                    if served:
                        break
                if not served:
                    print(f"  ✗ Tidak ada order dalam antrian\n")

            elif perintah == "CANCEL_LAST":
                last_order = order_stack.pop()
                if last_order:
                    canceled_orders.add(last_order.order_id)
                    tier_name = TIER_NAME[last_order.tier]
                    queues[tier_name].remove_by_condition(lambda o: o.order_id == last_order.order_id)
                    if last_order.pelanggan in cust_stacks:
                        cust_stacks[last_order.pelanggan].remove_by_condition(lambda o: o.order_id == last_order.order_id)
                    print(f"  ✓ CANCEL Order {last_order.order_id}: {last_order.pelanggan} - {last_order.produk_kode}")
                    print(f"  [O(1): Pop dari stack]\n")
                else:
                    print(f"  ✗ Tidak ada order untuk dibatalkan\n")

            elif perintah == "CARI_PRODUK" and len(parts) >= 2:
                kode = parts[1].upper()
                produk = bst_katalog.search(kode)
                if produk:
                    print(f"\n  Kode  : {produk.kode}")
                    print(f"  Nama  : {produk.nama}")
                    print(f"  Harga : Rp {produk.harga:,.0f}")
                    print(f"  Stok  : {produk.stok}")
                    print(f"  [O(log n): BST search]\n")
                else:
                    print(f"  ✗ Produk {kode} tidak ditemukan\n")

            elif perintah == "UPDATE_STOK" and len(parts) >= 3:
                kode = parts[1].upper()
                try:
                    qty = int(parts[2])
                    if bst_katalog.update_stok(kode, qty):
                        prod = bst_katalog.search(kode)
                        print(f"  ✓ UPDATE STOK {kode}: +{qty} → Stok baru: {prod.stok}")
                        print(f"  [O(log n): BST update]\n")
                    else:
                        print(f"  ✗ Produk {kode} tidak ditemukan\n")
                except ValueError:
                    print(f"  ✗ Qty harus berupa angka\n")

            elif perintah == "REKOMENDASI" and len(parts) >= 2:
                kode = parts[1].upper()
                recom = graph_rek.rekomendasi(kode, max_hop=2)
                if recom:
                    print(f"  Rekomendasi untuk {kode}: {', '.join(recom)}")
                    print(f"  [O(V+E): BFS graph]\n")
                else:
                    print(f"  Tidak ada rekomendasi untuk {kode}\n")

            elif perintah == "RIWAYAT" and len(parts) >= 2:
                pelanggan = parts[1]
                if pelanggan in cust_stacks:
                    stack = cust_stacks[pelanggan]
                    if stack.top:
                        print(f"\n  Riwayat Order {pelanggan}:")
                        node = stack.top
                        count = 0
                        while node and count < 10:
                            order = node.data
                            if order.order_id in canceled_orders:
                                node = node.next
                                continue
                            print(f"    {count+1}. Order {order.order_id} - {order.produk_kode} - Rp {order.total_harga:,.0f}")
                            node = node.next
                            count += 1
                        print(f"  [O(1): Stack traversal]\n")
                    else:
                        print(f"  ✗ {pelanggan} belum punya order\n")
                else:
                    print(f"  ✗ Pelanggan {pelanggan} tidak ditemukan\n")

            elif perintah == "LAPORAN_HARIAN":
                if not completed_orders:
                    print(f"  ✗ Tidak ada order yang selesai\n")
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
                print(f"  Terima kasih! Sampai jumpa.\n")
                break

            else:
                print(f"  ✗ Perintah '{perintah}' tidak dikenali. Ketik BANTUAN\n")

        except KeyboardInterrupt:
            print(f"\n  Program dihentikan.\n")
            break
        except Exception as e:
            print(f"  ✗ Error: {e}\n")

if __name__ == "__main__":
    main()
