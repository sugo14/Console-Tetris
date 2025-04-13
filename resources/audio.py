import winsound, time

class Audio:
    def __init__(self, bpm, notes):
        self.bpm = bpm * 1.5
        self.notes = notes

def format(filepath):
    with open(filepath, 'r') as f:
        bpm = int(f.readline().strip())
        notes = [(int(freq), float(duration)) for freq, duration in [line.strip().split() for line in f.readlines()]]
    return Audio(bpm, notes)

def play(audio):
    time.sleep(1)
    for note in audio.notes:
        f = note[0]
        t = 60 / audio.bpm * note[1]
        if f == 0:
            time.sleep(t)
        else:
            winsound.Beep(f, int(t * 1000))

play(format("resources/audio.txt"))
