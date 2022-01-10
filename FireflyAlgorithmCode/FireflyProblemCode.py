import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, cm
import operator

from FireflyCode import FireflyCode


def rosenbrock(x):
    ans = 0.0
    for i in range(min(len(x), 16)):
        ans += (100.0 * (x[i] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2)
    return ans


class FireflyProblemCode:
    def __init__(self, firefly_number, win, upper_boundary=5.12, lower_boundary=-5.12, alpha=2,
                 beta=2, gamma=0.97, iteration_number=50, interval=500, continuous=False):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.function_dimension = 2
        self.upper_boundary = upper_boundary
        self.lower_boundary = lower_boundary
        self.iteration_number = iteration_number
        self.fireflies = [
            FireflyCode(self.alpha, self.beta, self.gamma, self.upper_boundary, self.lower_boundary,
                        self.function_dimension) for x in range(firefly_number)]
        self.function = rosenbrock
        self.interval = interval
        self.best = None
        self.continuous = continuous
        self.cost = []
        self.win = win
        self.result = ''
        i = 0
        while i < (len(self.fireflies)):  # Change to while
            self.fireflies[i].update_intensity(self.function)
            i += 1

    def run(self):
        y = np.linspace(self.lower_boundary, self.upper_boundary, 100)
        x = np.linspace(self.lower_boundary, self.upper_boundary, 100)
        X, Y = np.meshgrid(x, y)
        z = self.function([X, Y])
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        cs = ax.contourf(X, Y, z, cmap=cm.PuBu_r)  # pylint: disable=no-member
        fig.colorbar(cs)
        x_init = []
        y_init = []
        i = 0
        while i < (len(self.fireflies)):  # change to while
            x_init.append(self.fireflies[i].position[0])
            y_init.append(self.fireflies[i].position[1])
            i += 1
        particles, = ax.plot(x_init, y_init, 'ro', ms=6)
        rectangle = plt.Rectangle([self.lower_boundary, self.lower_boundary],
                                  self.upper_boundary - self.lower_boundary,
                                  self.upper_boundary - self.lower_boundary, ec='none', lw=2, fc='none')
        ax.add_patch(rectangle)

        #         self.plot()

        def init():
            particles.set_data([], [])
            rectangle.set_edgecolor('none')
            return particles, rectangle

        def animate(i):  # Generate animation and visualization
            x = []
            y = []
            ms = int(50. * fig.get_figwidth() / fig.dpi)
            rectangle.set_edgecolor('k')

            if i == 0:
                print("reset the fireflies")
                self.best = None

            for idx, firefly in enumerate(self.fireflies):
                if i == 0:
                    firefly.__position = np.array([x_init[idx], y_init[idx]])
                    firefly.update_intensity(self.function)

                x.append(firefly.position[0])
                y.append(firefly.position[1])
            self.step()
            particles.set_data(x, y)
            particles.set_markersize(ms)
            return particles, rectangle

        graph = animation.FuncAnimation(fig, animate, frames=self.iteration_number + 1,
                                        interval=self.interval, blit=True, init_func=init,
                                        repeat=self.continuous)
        plt.show()
        if not self.best or self.fireflies[0].intensity > self.best:
            self.best = self.fireflies[0].intensity

        graph.save('firefly_rosenbrock.gif')
        resultLog = open("myfile.txt", "w")
        resultLog.write(self.result)

    def step(self):
        self.fireflies.sort(key=operator.attrgetter('intensity'), reverse=True)
        for i in self.fireflies:
            for j in self.fireflies:
                if j.intensity > i.intensity:
                    i.move_towards(j.position)
                    i.update_intensity(self.function)

        if not self.best or (self.fireflies[0].intensity > self.best):
            self.best = self.fireflies[0].intensity

        gmin = 0
        self.cost.append(abs(self.best - gmin))
        print("En iyi Yoğunluk: {}, En iyi Doğruluk: {}".format(self.best, 100 * abs(
            1 - abs(self.best - gmin))))
        self.result += "En iyi Yoğunluk: {}, En iyi Doğruluk: {}".format(self.best, 100 * abs(
            1 - abs(self.best - gmin))) + "\n"

    def plot(self):
        X_Axis = range(1, self.iteration_number + 2)
        plt.plot(X_Axis, self.cost)
        plt.xlabel('No. of iterations')
        plt.ylabel('Cost')
        plt.show()
