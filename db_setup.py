import sqlite3
import pandas as pd
import os

def setup_database():
    db_path = 'football.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop table if it exists to ensure idempotency
    cursor.execute('DROP TABLE IF EXISTS matches')

    # Create matches table
    cursor.execute('''
        CREATE TABLE matches (
            Div TEXT,
            Date TEXT,
            Time TEXT,
            HomeTeam TEXT,
            AwayTeam TEXT,
            FTHG INTEGER,
            FTAG INTEGER,
            FTR TEXT,
            HTHG INTEGER,
            HTAG INTEGER,
            HTR TEXT,
            "HS" INTEGER,
            "AS" INTEGER,
            HST INTEGER,
            AST INTEGER,
            HF INTEGER,
            AF INTEGER,
            HC INTEGER,
            AC INTEGER,
            HY INTEGER,
            AY INTEGER,
            HR INTEGER,
            AR INTEGER,
            B365H REAL,
            B365D REAL,
            B365A REAL,
            BWH REAL,
            BWD REAL,
            BWA REAL,
            "PSH" REAL,
            "PSD" REAL,
            "PSA" REAL,
            WHH REAL,
            WHD REAL,
            WHA REAL,
            MaxH REAL,
            MaxD REAL,
            MaxA REAL,
            AvgH REAL,
            AvgD REAL,
            AvgA REAL,
            "B365>2.5" REAL,
            "B365<2.5" REAL,
            "P>2.5" REAL,
            "P<2.5" REAL,
            "Max>2.5" REAL,
            "Max<2.5" REAL,
            "Avg>2.5" REAL,
            "Avg<2.5" REAL,
            "AHh" REAL,
            B365AHH REAL,
            B365AHA REAL,
            PAHH REAL,
            PAHA REAL,
            MaxAHH REAL,
            MaxAHA REAL,
            AvgAHH REAL,
            AvgAHA REAL,
            B365CH REAL,
            B365CD REAL,
            B365CA REAL,
            BWCH REAL,
            BWCD REAL,
            BWCA REAL,
            PSCH REAL,
            PSCD REAL,
            PSCA REAL,
            WHCH REAL,
            WHCD REAL,
            WHCA REAL,
            MaxCH REAL,
            MaxCD REAL,
            MaxCA REAL,
            AvgCH REAL,
            AvgCD REAL,
            AvgCA REAL,
            "B365C>2.5" REAL,
            "B365C<2.5" REAL,
            "PC>2.5" REAL,
            "PC<2.5" REAL,
            "MaxC>2.5" REAL,
            "MaxC<2.5" REAL,
            "AvgC>2.5" REAL,
            "AvgC<2.5" REAL,
            AHCh REAL,
            B365CAHH REAL,
            B365CAHA REAL,
            PCAHH REAL,
            PCAHA REAL,
            MaxCAHH REAL,
            MaxCAHA REAL,
            AvgCAHH REAL,
            AvgCAHA REAL
        )
    ''')
    conn.commit()

    # Load data from dataset.csv
    try:
        df = pd.read_csv('data/dataset.csv')
        df.to_sql('matches', conn, if_exists='append', index=False)
        print("Historical data loaded successfully.")
    except FileNotFoundError:
        print("Error: dataset.csv not found. Please ensure it's in the 'data/' directory.")
    except Exception as e:
        print(f"An error occurred during data loading: {e}")

    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
