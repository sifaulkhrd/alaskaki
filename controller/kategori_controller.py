from models import produk
from models import kategori

def kategori_id_produk_controller(kategori_id):
    """
    Kontroler untuk mendapatkan produk berdasarkan ID kategori.

    Args:
    - kategori_id (int): ID kategori yang dicari.

    Returns:
    - dict: Dictionary berisi informasi kategori (id, nama, dan produk terkait) jika ditemukan,
      atau pesan kesalahan jika tidak ditemukan.
    """
    if produk.get_produk_by_kategori(kategori_id) is None:
        return {'message': 'Kategori tidak ditemukan'}

    list_produk = produk.get_produk_by_kategori(kategori_id)
    list_kategori = kategori.get_kategori_by_id(kategori_id)

    if list_produk is None:
        list_kategori["produk"] = "Belum ada produk di kategori ini"
    else:
        list_kategori["produk"] = list_produk

    return list_kategori


def kategori_by_id(id):
    """
    Mendapatkan kategori beserta produk yang terkait berdasarkan ID.

    Args:
    - id (int): ID kategori yang dicari.

    Returns:
    - dict or HTTP Response: Dictionary berisi informasi kategori (id, nama, dan produk terkait) jika ditemukan,
      atau respons dengan pesan kesalahan jika tidak ditemukan.
    """
    item = kategori.get_kategori_by_id(id)
    if item is None:
        return {'message': 'Kategori tidak ditemukan'}, 402

    # Get all products associated with the category
    produk_terkait = produk.get_all_produk(id)
    item["produk"] = produk_terkait

    return item
