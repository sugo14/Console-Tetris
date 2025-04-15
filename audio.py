import winsound, time

class Audio:
    def __init__(self, bpm, notes):
        self.bpm = bpm * 1
        self.notes = notes

    def compile(filename):
        with open(f"resources/{filename}.txt", 'r') as f:
            bpm = int(f.readline().strip())
            notes = [(int(freq), float(duration)) for freq, duration in [line.strip().split() for line in f.readlines()]]
        return Audio(bpm, notes)
    
    def play(self):
        for note in self.notes:
            f = note[0]
            t = 60 / self.bpm * note[1]
            if f == 0:
                time.sleep(t)
            else:
                winsound.Beep(f, int(t * 1000))

if __name__ == "__main__":
    Audio.compile("main_song").play()
