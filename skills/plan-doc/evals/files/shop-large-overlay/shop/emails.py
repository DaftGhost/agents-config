OUTBOX = []


def send(to, subject, body):
    OUTBOX.append((to, subject, body))
