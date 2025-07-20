import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Parameters
n_users = 1000
n_days = 90 # approx 3 months
start_date = datetime.today() - timedelta(days=n_days)

# Generate list of user_ids
user_ids = [f"user_{i}" for i in range(1, n_users + 1)]

# Generate data
records = []
for user_id in user_ids:
    num_sessions = np.random.poisson(15) # average 15 sessions per 3 months
    session_dates = sorted(random.choices([start_date + timedelta(days=i) for i in range(n_days)], k=num_sessions))
    last_login = session_dates[-1] if session_dates else None
    
    for date in session_dates:
        session_duration = np.random.exponential(scale=10) # average 10 mins
        num_videos = np.random.poisson(7)
        num_likes = np.random.binomial(num_videos, 0.3)
        num_comments = np.random.binomial(num_videos, 0.1)
        retention = int((last_login - date).days <= 7) if last_login else 0

        records.append({
            'user_id': user_id,
            'session_date': date.date(),
            'session_duration_min': round(session_duration, 2),
            'videos_watched': num_videos,
            'likes': num_likes,
            'comments': num_comments,
            'is_retained_7d': retention,
        })

# Create DataFrame
df = pd.DataFrame(records)

# Save to CSV
output_path = "data/raw/synthetic_user_data.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

print(f"Generated {len(df)} rows of synthetic user data saved to {output_path}")
