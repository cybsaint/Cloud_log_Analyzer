"""Simple CLI for the Cloud Security Log Analyzer scaffold.

This script demonstrates basic file handling, functions, and module usage.
Run: `python3 main.py` to print a few analysis results.
"""
from src.log_reader import read_logs
from src.analyzer import (
	count_events_by_type,
	count_events_by_level,
	failed_logins_by_user,
	detect_brute_force,
	top_active_users,
	summarize_alerts,
)


def main():
	path = "cloud_log.txt"
	print(f"Reading logs from {path}...\n")
	records = read_logs(path)

	print("Top event types:")
	for event, cnt in count_events_by_type(records).most_common(10):
		print(f" - {event}: {cnt}")

	print("\nLog levels:")
	for level, cnt in count_events_by_level(records).items():
		print(f" - {level}: {cnt}")

	print("\nFailed logins by user:")
	for user, cnt in failed_logins_by_user(records).items():
		print(f" - {user}: {cnt}")

	print("\nBrute-force suspects:")
	for ident, cnt in detect_brute_force(records):
		print(f" - {ident}: {cnt}")

	print("\nTop active users:")
	for user, cnt in top_active_users(records):
		print(f" - {user}: {cnt}")

	print("\nAlerts summary:")
	for a in summarize_alerts(records):
		print(f" - {a.get('timestamp')} {a.get('event')} {a})")


if __name__ == "__main__":
	main()

