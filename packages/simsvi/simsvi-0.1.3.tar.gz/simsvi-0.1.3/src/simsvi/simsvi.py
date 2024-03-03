import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import pandas as pd
import matplotlib.colors as mcolors
import warnings


class SVISimulation:
    def __init__(
        self,
        size=31,
        green_max=1,
        green_min=0,
        road_width=0.5,
        tree_ratio=0.1,
        camera_position_range=1,
        hot_month=7,
        cold_month=1,
        tree_change=[0.1, -0.1],
        dir_plot=False,
        months_of_interest=None,  # Add this parameter
        seed=42,
    ):
        self.seed = seed
        np.random.seed(seed)
        self.size = size
        self.layer_weights = self.calculate_layer_weights()
        self.expanded_scenario_size = (
            size + 2 * camera_position_range,
            size,
        )  # Add padding only in y-axis
        self.green_max = green_max
        self.green_min = green_min
        self.road_width = road_width
        self.tree_ratio = tree_ratio
        # make sure that camera_position_range is not larger than the size of the scenario
        if camera_position_range > size // 2:
            raise ValueError(
                "camera_position_range should not be larger than the size of the scenario"
            )
        self.camera_position_range = camera_position_range
        self.hot_month = hot_month
        self.cold_month = cold_month
        self.tree_change = tree_change
        self.month = 1
        self.year = 1
        self.camera_position = (
            size // 2 + camera_position_range,
            size // 2,
        )  # Center position in the original scenario
        self.greenery_dict_list = []
        self.tree_positions = []
        self.dir_plot = dir_plot
        self.seed = seed
        self.months_of_interest = (
            months_of_interest if months_of_interest else list(range(1, 13))
        )
        self.create_expanded_scenario()

    def create_expanded_scenario(self):
        # Identify all possible positions for trees avoiding the road
        possible_positions = set(
            [
                (x, y)
                for x in range(self.expanded_scenario_size[0])
                for y in range(self.expanded_scenario_size[1])
                if not (
                    self.size // 2 - int(self.size * self.road_width // 2)
                    <= y
                    <= self.size // 2 + int(self.size * self.road_width // 2)
                )
            ]
        )
        self.possible_positions = possible_positions
        # Reset the scenario
        self.expanded_scenario = np.zeros(self.expanded_scenario_size)
        # pick a random position for the trees by tree_ratio
        num_trees = int(self.tree_ratio * len(possible_positions))
        positions = set()
        while len(positions) < num_trees:
            x = np.random.randint(0, self.expanded_scenario_size[0])
            y = np.random.randint(0, self.expanded_scenario_size[0])
            # Ensure trees are not placed on the road
            if (x, y) in possible_positions and (x, y) not in positions:
                positions.add((x, y))
        self.tree_positions = list(positions)
        for pos in self.tree_positions:
            self.expanded_scenario[pos] = self.green_min  # Initial greenery level

    def calculate_layer_weights(self):
        max_layers = self.size // 2
        layer_weight = 1 / max_layers
        layer_weights = {}

        for layer in range(
            1, max_layers + 1
        ):  # Start from 1 to exclude the center layer
            num_cells_in_layer = (
                layer * 8
            )  # Calculate the number of cells in each layer
            layer_weights[layer] = (
                layer_weight / num_cells_in_layer
            )  # Weight per cell in the layer

        return layer_weights

    def calculate_occlusion_factors(self, tree_positions, camera_position):
        def convert_to_polar(coords):
            delta = coords - camera_position
            r = np.linalg.norm(delta, axis=1)
            theta = np.arctan2(delta[:, 1], delta[:, 0])
            return np.vstack((theta, r)).T

        def group_by_angle(polar_trees):
            # Use a dictionary to group trees by their angle
            groups = {}
            for idx, (theta, r) in enumerate(polar_trees):
                if theta not in groups:
                    groups[theta] = []
                groups[theta].append((idx, r))
            return groups

        polar_trees = convert_to_polar(tree_positions)
        angle_groups = group_by_angle(polar_trees)

        occlusion_factors = np.ones(len(tree_positions))
        for angle, group in angle_groups.items():
            # Sort the group by distance
            sorted_group = sorted(group, key=lambda x: x[1])
            visible_tree_distance = 0
            for idx, r in sorted_group:
                if r > visible_tree_distance:
                    # Assuming simple occlusion logic; refine based on your needs
                    visible_tree_distance = r
                    occlusion_factors[idx] = 1  # Fully visible
                else:
                    # This tree is occluded by a closer tree
                    occlusion_factors[idx] = 0  # Fully occluded

        return occlusion_factors

    def get_greenery(self):
        tree_positions = np.array(self.tree_positions)
        camera_position = np.array(self.camera_position)

        # Calculate Manhattan distances and determine layers
        layers = np.abs(tree_positions - camera_position).max(axis=1)

        # Apply visual range mask
        visual_range_mask = layers <= self.size // 2
        layers_in_range = layers[visual_range_mask]

        # Map each tree's layer to its corresponding weight
        weights = np.vectorize(self.layer_weights.get)(layers_in_range)

        # Calculate occlusion factors for trees within the visual range
        occlusion_proportions = self.calculate_occlusion_factors(
            tree_positions[visual_range_mask], camera_position
        )

        # Compute visibility contributions and sum them up
        visibility_contributions = (
            weights
            * occlusion_proportions
            * self.expanded_scenario[
                tree_positions[visual_range_mask][:, 0],
                tree_positions[visual_range_mask][:, 1],
            ]
        )
        total_visibility = visibility_contributions.sum()

        return total_visibility

    # def calculate_layer_counts(self, distances):
    #     # Vectorized layer count calculation based on Manhattan distance
    #     return np.maximum(1, 8 * distances).astype(int)

    # def calculate_dynamic_occlusion(self, target_pos, tree_positions):
    #     # Calculate occlusion based on the positions of other trees relative to the target tree
    #     target_index = np.where((tree_positions == target_pos).all(axis=1))[0][0]
    #     occlusion = 1.0
    #     for i, pos in enumerate(tree_positions):
    #         if i == target_index:
    #             continue  # Skip the target tree itself
    #         occlusion *= (1 - self.calculate_occlusion_factor(target_pos, pos))
    #     return max(0, occlusion)

    # def calculate_occlusion_factor(self, target_tree_pos, other_tree_pos):
    #     """
    #     Calculate how much other_tree_pos occludes target_tree_pos.
    #     Returns a factor between 0 (no occlusion) and 1 (full occlusion).
    #     """
    #     target_angle, target_distance = self.angle_and_distance_to_camera(
    #         target_tree_pos
    #     )
    #     other_angle, other_distance = self.angle_and_distance_to_camera(other_tree_pos)

    #     if other_distance >= target_distance:
    #         return 0  # Cannot occlude if it's not closer to the camera

    #     angle_difference = abs(target_angle - other_angle)
    #     distance_difference = target_distance - other_distance

    #     # Example occlusion calculation, can be adjusted
    #     angle_threshold = self.calculate_angle_threshold(
    #         target_distance, other_distance
    #     )
    #     if angle_difference > angle_threshold:
    #         return 0  # No occlusion if outside angle threshold

    #     # Simplified partial occlusion model
    #     occlusion_factor = (1 - (angle_difference / angle_threshold)) * (
    #         1 - distance_difference / target_distance
    #     )
    #     return occlusion_factor

    # def angle_and_distance_to_camera(self, tree_pos):
    #     """
    #     Calculate the angle and Manhattan distance from the camera to tree_pos.
    #     """
    #     camera_x, camera_y = self.camera_position
    #     tree_x, tree_y = tree_pos
    #     angle = math.atan2(tree_y - camera_y, tree_x - camera_x)
    #     distance = abs(camera_x - tree_x) + abs(camera_y - tree_y)  # Manhattan distance
    #     return angle, distance

    # def calculate_angle_threshold(self, tree_distance, other_tree_distance):
    #     """
    #     Determines the angle within which another tree can occlude the target tree.
    #     Adjust based on simulation specifics.
    #     """
    #     base_angle = math.radians(5)  # Example threshold
    #     return base_angle / max(1, abs(tree_distance - other_tree_distance))

    def update_scenario(self):
        # Iterate through each tree position to update its greenery value based on the month
        for x, y in self.tree_positions:
            # Normalize months to radians, with January as 0 and December as 2π
            month_radians = 2 * np.pi * (self.month - 1) / 12

            # Calculate the phase shift needed to align the peak with hot_month
            # π/2 is the peak of the sine wave, adjust it to align with hot_month
            hot_month_radians = 2 * np.pi * (self.hot_month - 1) / 12
            phase_shift_to_hot = (np.pi / 2) - hot_month_radians

            # Adjust the month's radians by the phase shift for alignment
            adjusted_radians = month_radians + phase_shift_to_hot

            # Sine function to simulate seasonal variation, with output range [-1, 1]
            sine_value = np.sin(adjusted_radians)

            # Adjust the sine_value directly to align the trough with cold_month if necessary
            # This step is optional and depends on specific requirements for cold_month alignment

            # Map sine output from [-1, 1] to [green_min, green_max]
            greenery_value = ((sine_value + 1) / 2) * (
                self.green_max - self.green_min
            ) + self.green_min

            # Update the current scenario with the calculated greenery value
            self.expanded_scenario[x, y] = greenery_value

    def update_tree_position(self):
        # Calculate the number of trees to add based on tree_change for the current year
        change_rate = self.tree_change[self.year - 1]

        # Remove current tree positions from possible positions
        possible_positions = [
            pos for pos in self.possible_positions if pos not in self.tree_positions
        ]

        if change_rate > 0:
            # Calculate how many new trees to add
            trees_to_add = int(len(self.tree_positions) * change_rate)
            if trees_to_add > len(possible_positions):
                warnings.warn(
                    "Not enough space to add more trees. Adding as many as possible."
                )
                trees_to_add = len(possible_positions)

            # Add new trees
            new_positions = np.random.choice(
                range(len(possible_positions)), size=trees_to_add, replace=False
            )
            for index in new_positions:
                self.tree_positions.append(possible_positions[index])
        elif change_rate < 0:
            # Calculate how many trees to remove
            trees_to_remove = int(len(self.tree_positions) * abs(change_rate))
            if trees_to_remove > 0:
                removed_positions = np.random.choice(
                    range(len(self.tree_positions)), size=trees_to_remove, replace=False
                )
                self.tree_positions = [
                    self.tree_positions[i]
                    for i in range(len(self.tree_positions))
                    if i not in removed_positions
                ]

    def generate_camera_positions(self):
        # Generate all possible camera positions within the specified range around the original position
        original_x, original_y = (
            self.size // 2 + self.camera_position_range * 2,
            self.size // 2,
        )  # Center
        positions = [
            (x, y)
            for x in range(
                original_x - self.camera_position_range,
                original_x + self.camera_position_range + 1,
            )
            for y in range(
                original_y - self.camera_position_range,
                original_y + self.camera_position_range + 1,
            )
        ]
        return positions

    def run_simulation(self):
        # Adjust camera position within the specified range during simulation
        for year in range(1, len(self.tree_change) + 2):
            self.year = year
            for month in range(1, 13):
                self.month = month
                if (
                    self.month in self.months_of_interest
                ):  # Check if the month is of interest
                    camera_positions = self.generate_camera_positions()
                    for cam_pos in camera_positions:
                        self.camera_position = cam_pos
                        self.update_scenario()
                        if len(self.tree_positions) > 0:
                            visible_greenery = self.get_greenery()
                        else:
                            visible_greenery = 0
                        self.greenery_dict_list.append(
                            {
                                "seed": self.seed,
                                "size": self.size,
                                "green_max": self.green_max,
                                "green_min": self.green_min,
                                "road_width": self.road_width,
                                "tree_ratio": self.tree_ratio,
                                "camera_position_range": self.camera_position_range,
                                "hot_month": self.hot_month,
                                "cold_month": self.cold_month,
                                "tree_change": self.tree_change,
                                "dir_plot": self.dir_plot,
                                # Simulation specific data
                                "year": year,
                                "month": month,
                                "camera_position_x": cam_pos[0],
                                "camera_position_y": cam_pos[1],
                                "green_view_index": visible_greenery,
                            }
                        )
                        if self.dir_plot:
                            self.plot_scenario()
            # run if not the last year
            if year < len(self.tree_change) + 1:
                self.update_tree_position()
        if self.dir_plot:
            self.plot_green_view_index_over_time()

    def plot_green_view_index_over_time(self):
        # Convert greenery_dict_list to DataFrame
        df = pd.DataFrame(self.greenery_dict_list)
        df["year_month"] = (
            df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)
        )
        df["camera_position"] = df.apply(
            lambda x: f"{x['camera_position_x']},{x['camera_position_y']}", axis=1
        )

        fig, ax = plt.subplots(figsize=(14, 8))
        for camera_position, group in df.groupby("camera_position"):
            group = group.sort_values(by=["year", "month"])
            ax.plot(
                group["year_month"],
                group["green_view_index"],
                marker="o",
                linestyle="-",
                label=camera_position,
            )

        ax.set_xlabel("Year and Month")
        ax.set_ylabel("Green View Index")
        ax.set_title("Green View Index over Time by Camera Position")
        plt.xticks(rotation=45)
        ax.legend(title="Camera Position", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()

        # Save plot to directory
        if self.dir_plot:
            os.makedirs(self.dir_plot, exist_ok=True)
            plt.savefig(f"{self.dir_plot}/green_view_index_over_time.png")
        plt.close()

    def plot_scenario(self):
        fig, ax = plt.subplots()
        # Define the colormap and normalization for greenery values
        cmap = plt.get_cmap("Greens")
        norm = mcolors.Normalize(vmin=self.green_min, vmax=self.green_max)

        # Display the scenario
        scenario_image = ax.imshow(self.expanded_scenario, cmap=cmap, norm=norm)

        # Add colorbar for greenery density
        cbar = fig.colorbar(
            scenario_image,
            ax=ax,
            orientation="horizontal",
            pad=0.1,
            fraction=0.046,
            label="Greenery Density",
        )

        # Paint the road part in gray
        road_start = self.size // 2 - int(self.size * self.road_width // 2)
        road_width = int(self.size * self.road_width)
        ax.add_patch(
            Rectangle(
                (road_start, 0),
                road_width,
                self.expanded_scenario_size[0],
                color="gray",
                alpha=0.5,
            )
        )

        # Mark the camera position
        ax.add_patch(
            Rectangle(
                (self.camera_position[1] - 0.5, self.camera_position[0] - 0.5),
                1,
                1,
                linewidth=2,
                edgecolor="r",
                facecolor="none",
            )
        )

        ax.set_title(
            f"Scenario: Year {self.year}, Month {self.month}, Camera Position {self.camera_position}"
        )

        # Create custom patches for the legend
        camera_patch = Rectangle((0, 0), 1, 1, color="r", label="Camera")
        road_patch = Rectangle((0, 0), 1, 1, color="gray", alpha=0.5, label="Road")

        # Place the legend outside the plot
        legend = ax.legend(
            handles=[camera_patch, road_patch],
            loc="upper left",
            bbox_to_anchor=(1, 1),
            title="Legend",
        )

        os.makedirs(self.dir_plot, exist_ok=True)
        plt.savefig(
            f"{self.dir_plot}/scenario_year_{self.year}_month_{self.month}_camX{self.camera_position[0]}_camY{self.camera_position[1]}.png"
        )
        plt.close(fig)
