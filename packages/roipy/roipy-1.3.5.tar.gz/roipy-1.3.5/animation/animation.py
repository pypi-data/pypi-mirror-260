from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Anim(object):
    """Animation class
    
    Parameters
    ----------
    frames: int
    
    fps: int
        Frames per second
    
    interval: int
    
    Return
    ------
    """

    frames: int = 15
    fps: int = 10
    interval: int = 200

    def animate(self, func, fname: str, figsize: tuple, save=True):
        """Animate method

        func: function

        fname: str
            Filename
            Include '.gif' file extension
        
        figsize: tuple
            
        save: bool
            Save the animation?
        """
        fig = plt.figure(figsize=figsize)

        def update(frame):
            plt.clf()
            return func(frame)

        anim = FuncAnimation(fig, update, frames=self.frames, blit=False, repeat=False)

        if save:
            anim.save(fname, writer='imagemagick')

        plt.show()

        return anim
