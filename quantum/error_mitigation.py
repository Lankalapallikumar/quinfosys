def mitigate_noise(counts, threshold=50):
    filtered = {k: v for k, v in counts.items() if v > threshold}
    total = sum(filtered.values())

    return {k: v / total for k, v in filtered.items()}