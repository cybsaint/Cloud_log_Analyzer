"""Module providing simple analysis helpers for cloud security logs.

This file demonstrates functions, loops, control flow, and basic data types.
"""
from typing import List, Dict, Tuple
from collections import Counter


def count_events_by_type(records: List[Dict[str, str]]) -> Counter:
	return Counter(r.get("event", "UNKNOWN") for r in records)


def count_events_by_level(records: List[Dict[str, str]]) -> Counter:
	return Counter(r.get("level", "UNKNOWN") for r in records)


def failed_logins_by_user(records: List[Dict[str, str]]) -> Dict[str, int]:
	c = Counter()
	for r in records:
		if r.get("event") == "LOGIN_FAILED":
			user = r.get("user", "<unknown>")
			c[user] += 1
	return dict(c)


def detect_brute_force(records: List[Dict[str, str]], threshold: int = 4) -> List[Tuple[str, int]]:
	by_user = Counter()
	by_ip = Counter()
	for r in records:
		if r.get("event") == "LOGIN_FAILED":
			by_user[r.get("user", "<unknown>")] += 1
			if "ip" in r:
				by_ip[r["ip"]] += 1
		if r.get("event") == "BRUTE_FORCE_DETECTED":
			if "target" in r:
				by_user[r["target"]] += 1
			if "ip" in r:
				by_ip[r["ip"]] += 1

	suspects: List[Tuple[str, int]] = []
	for user, cnt in by_user.items():
		if cnt >= threshold:
			suspects.append((f"user:{user}", cnt))
	for ip, cnt in by_ip.items():
		if cnt >= threshold:
			suspects.append((f"ip:{ip}", cnt))

	suspects.sort(key=lambda x: x[1], reverse=True)
	return suspects


def top_active_users(records: List[Dict[str, str]], n: int = 5) -> List[Tuple[str, int]]:
	c = Counter()
	for r in records:
		user = r.get("user")
		if user:
			c[user] += 1
	return c.most_common(n)


def summarize_alerts(records: List[Dict[str, str]]) -> List[Dict[str, str]]:
	return [r for r in records if r.get("level") == "ALERT"]


__all__ = [
	"count_events_by_type",
	"count_events_by_level",
	"failed_logins_by_user",
	"detect_brute_force",
	"top_active_users",
	"summarize_alerts",
]


if __name__ == "__main__":
	# quick demo when run directly
	from src.log_reader import read_logs
	recs = read_logs("../cloud_log.txt")
	print("Event counts:", count_events_by_type(recs))
	print("Level counts:", count_events_by_level(recs))
