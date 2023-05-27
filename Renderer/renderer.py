# Library imports

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg
import cv2
import numpy as np
import networkx as nx
import sys
import os
import random

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map
#from Map.map import * # Dårlig kodeskik at importere en hel fil

class Renderer:
    def __init__(self, map: Map, delay=0.0001, fig_size_factor=15, node_size=12, linewidth=0.5, dpi=400, colors={"background": "white", "obstacle": "black", "agent": "blue", "target": "lightgreen"}):
        self.map = map
        self.colors = colors
        self._display_initialized = False
        self.frames = []
        self.delay = delay
        
        self.fig_size_factor = fig_size_factor
        self.fig_size = (self.map.map_width / fig_size_factor, self.map.map_height / fig_size_factor)
        self.node_size = node_size
        self.linewidth = linewidth
        self.dpi = dpi
        #(self.map.map_width / 4, self.map.map_height / 4)
        
    def plot_map_once(self):
        """ Show the world
        """
        color = []

        for _, data in list(self.map.map.nodes.data()): #error was name space related
            c = ""
            if "target" in data:
                if data["target"] is not None and data["agent"] is None:
                    #c = self.colors["target"]
                    #c = data["target"]
                    c = self.colors["background"]
                elif data["target"] is not None and data["agent"] is not None:
                    c = data["agent"].color
                    #c = self.colors["agent"]
                else:
                    c = self.colors["background"]
            elif "agent" in data:
                if data["agent"] is not None:  # added not
                    c = data["agent"].color
                    #c = self.colors["agent"]
                    #c = random.choice([col for col in plt.cm.tab20.colors if col != (0.0, 0.0, 0.0) and col != (1.0, 1.0, 1.0)])
                else:
                    c = self.colors["background"]
            elif "obstacle" in data:
                c = self.colors["obstacle"]
            else:
                c = self.colors["background"]

            color.append(c)


        pos = {n: (n[0] * 10, n[1] * 10) for n in nx.nodes(self.map.map)}  # again name space

        # nodes_graph = nx.draw_networkx_nodes(self.map.map, pos=pos, node_color=color,
        #                                      node_size=160, node_shape="s", linewidths=1.0)
        nodes_graph = nx.draw_networkx_nodes(self.map.map, pos=pos, node_color=color, node_size=self.node_size, node_shape="s", linewidths=self.linewidth)

        nodes_graph.set_edgecolor('black')

    def display_frame(self, step: int):
        """
        Display a frame
        """
        plt.clf()
        if not self._display_initialized:
            f = plt.gcf()
            #f.set_size_inches(self.map.map_width / 4, self.map.map_height / 4,
            #                  forward=True)
            f.set_size_inches(self.fig_size, forward=True)
            #f.set_dpi(1000)
            self._display_initialized = True

        plt.title(f"Step: {step}")
        self.plot_map_once()
        plt.draw()
        plt.show(block=False)
        plt.pause(self.delay)
        #plt.pause(5)

        
        plt.savefig("tmp_frame.png", dpi=self.dpi)
        frame = cv2.imread("tmp_frame.png")
        #up_points = (1920, 1080)
        #resized_up = cv2.resize(frame, up_points, interpolation= cv2.INTER_LINEAR)
        self.frames.append(frame)


    def create_animation(self, filename='test_animation.mp4', fps=10):
        # Get the height and width of the first image
        img = self.frames[0]
        height, width, layers = img.shape

        # Create the video writer object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(filename, fourcc, fps, (width,height))

        # Iterate through each image and add it to the video
        for png in self.frames:
            video_frame = cv2.cvtColor(png, cv2.COLOR_RGBA2RGB)
            video.write(video_frame)

        # Release the video writer
        video.release()


