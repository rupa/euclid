from midi import EuclideanSequence


def demo():
    seq = EuclideanSequence(5, 8, 0.2, 0.1)
    seq.play()
