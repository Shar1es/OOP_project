from db import get_connection

def insert_tree(species, height, diameter, location):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trees (species, height, diameter, location)
        VALUES (?, ?, ?, ?)
    """, (species, height, diameter, location))

    conn.commit()
    conn.close()


def get_all_trees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM trees")
    trees = cursor.fetchall()

    conn.close()
    return trees