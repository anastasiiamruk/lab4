import sqlite3

DB_NAME = "lab3.db"


class Block:
    def __init__(self, id, view, desc, img):
        self.id = id
        self.view = view
        self.desc = desc
        self.img = img

    def __str__(self):
        return f"Block(id={self.id}, view={self.view}, desc={self.desc})"

    @staticmethod
    def select_all():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM BLOCKS")
        rows = cursor.fetchall()

        conn.close()
        return [Block(*row) for row in rows]

    @staticmethod
    def get_block_vote_count():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            B.id,
            B.desc,
            COUNT(V.block_id) as vote_count
        FROM BLOCKS B
        LEFT JOIN VOTES V ON B.id = V.block_id
        GROUP BY B.id
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows


class Person:
    def __init__(self, id, name, addr):
        self.id = id
        self.name = name
        self.addr = addr

    def __str__(self):
        return f"Person(id={self.id}, name={self.name}, addr={self.addr})"

    @staticmethod
    def select_all():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM PERSONS")
        rows = cursor.fetchall()

        conn.close()
        return [Person(*row) for row in rows]

    @staticmethod
    def get_top_voters():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            P.name,
            COUNT(V.voter_id) as votes
        FROM PERSONS P
        JOIN VOTES V ON P.id = V.voter_id
        GROUP BY P.id
        ORDER BY votes DESC
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows


class Source:
    def __init__(self, id, ip_addr, country_code):
        self.id = id
        self.ip_addr = ip_addr
        self.country_code = country_code

    def __str__(self):
        return f"Source(id={self.id}, ip={self.ip_addr}, country={self.country_code})"

    @staticmethod
    def select_all():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM SOURCES")
        rows = cursor.fetchall()

        conn.close()
        return [Source(*row) for row in rows]


class Vote:
    def __init__(self, block_id, voter_id, timestamp, source_id):
        self.block_id = block_id
        self.voter_id = voter_id
        self.timestamp = timestamp
        self.source_id = source_id

    def __str__(self):
        return f"Vote(block={self.block_id}, voter={self.voter_id}, time={self.timestamp}, source={self.source_id})"

    @staticmethod
    def select_all():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM VOTES")
        rows = cursor.fetchall()

        conn.close()
        return [Vote(*row) for row in rows]

    @staticmethod
    def get_votes_with_details():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            V.block_id,
            P.name,
            V.timestamp,
            S.ip_addr,
            S.country_code
        FROM VOTES V
        JOIN PERSONS P ON V.voter_id = P.id
        JOIN SOURCES S ON V.source_id = S.id
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows


if __name__ == "__main__":

    print("=== ALL BLOCKS ===")
    for b in Block.select_all():
        print(b)

    print("\n=== ALL PERSONS ===")
    for p in Person.select_all():
        print(p)

    print("\n=== ALL SOURCES ===")
    for s in Source.select_all():
        print(s)

    print("\n=== ALL VOTES ===")
    for v in Vote.select_all():
        print(v)

    print("\n=== VOTES WITH DETAILS (JOIN) ===")
    for row in Vote.get_votes_with_details():
        print(row)

    print("\n=== VOTES PER BLOCK (GROUP BY) ===")
    for row in Block.get_block_vote_count():
        print(row)

    print("\n=== TOP VOTERS ===")
    for row in Person.get_top_voters():
        print(row)