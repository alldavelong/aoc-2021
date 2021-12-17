#!/usr/bin/env python3

range_x = tuple((235,259))
range_y = tuple((-118,-62))

test_x = tuple((20,30))
test_y = tuple((-10,-5))
# range_x, range_y = test_x, test_y

target = {
    'xmin': min(range_x),
    'xmax': max(range_x),
    'ymin': min(range_y),
    'ymax': max(range_y)
}

class Probe:
    def __init__(self, velocity_x, velocity_y, target:dict) -> None:
        self.velocity_x, self.velocity_y = velocity_x, velocity_y
        self.init_x, self.init_y = velocity_x, velocity_y
        self.pos_x, self.pos_y = 0, 0
        self.max_pos_y = 0
        self.target = target

    def __update_position(self) -> None:
        self.pos_x, self.pos_y = self.pos_x + self.velocity_x, self.pos_y + self.velocity_y
        if self.pos_y > self.max_pos_y:
            self.max_pos_y = self.pos_y

    def __update_velocity(self) -> None:
        change_x = 0 # won't change if velocity_x == 0
        if self.velocity_x > 0:
            change_x = -1
        elif self.velocity_x < 0:
            change_x = 1
        self.velocity_x += change_x
        self.velocity_y -= 1

    def __step(self) -> None:
        self.__update_position()
        self.__update_velocity()

    def __is_within_target_zone(self) -> bool:
        return (
                self.pos_x >= self.target['xmin']
                and self.pos_x <= self.target['xmax']
                and self.pos_y >= self.target['ymin']
                and self.pos_y <= self.target['ymax']
            )

    def __can_y_still_reach_target(self) -> bool:
        """return False if pos_y is already below the target zone (it can't increase)"""
        return not (self.pos_y < self.target['ymin'] and self.velocity_y < 0)

    def __can_x_still_reach_target(self) -> bool:
        """return False if pos_x is outside the target zone and not changing anymore (if velocity_x == 0)"""
        if self.velocity_x != 0:
            return True
        absolute_targets = [
            abs(self.target['xmin']),
            abs(self.target['xmax'])
            ]
        if (
            all(
                [abs(self.pos_x) < abs_target
                for abs_target in absolute_targets]
            )
            or all(
                [abs(self.pos_x) > abs_target
                for abs_target in absolute_targets]
        )):
            return False
        return True

    def __find_target_zone(self) -> bool:
        while True:
            if self.__is_within_target_zone():
                return True
            if not self.__can_y_still_reach_target():
                return False
            if not self.__can_x_still_reach_target():
                return False            
            self.__step()
    
    @staticmethod
    def check_all_possible_launches() -> list:
        probe, successful_probes = None, []
        y_try = 0
        while (
            y_try <= abs(target['ymin']) # if y_try > abs(ymin): target zone will be jumped over both starting down (y<0) and returning down after starting up (y>0)
            or y_try <= target['ymax'] # if ymin<0 and ymax>0 and ymax>abs(ymin): also check all y_try up until ymax
        ):
            x_try = 0
            while abs(x_try) <= abs(target['xmax']):
                # print(x_try, y_try)
                probe = Probe(x_try, y_try, target)
                if probe.__find_target_zone():
                    successful_probes.append(probe)
                x_try += 1
            if y_try > 0:
                y_try *= -1
            else:
                y_try *= -1
                y_try += 1
        return successful_probes

successful_probes = Probe.check_all_possible_launches()

def part1():
    # probe = Probe(7,2, target)
    # print(probe.find_target_zone())
    # print(probe.pos_x, probe.pos_y, probe.max_pos_y)

    max_y_pos, max_probe = 0, None
    for probe in successful_probes:
        if probe.max_pos_y > max_y_pos:
            max_y_pos = probe.max_pos_y
            max_probe = probe
    print('lauching probe with velocity (%d, %d) reaches highest y position of %d (while also hitting the target)' % (max_probe.init_x, max_probe.init_y, max_y_pos))

def part2():
    print('number of different initial velocities that hit the target: %d' % len(successful_probes))

part1()
part2()