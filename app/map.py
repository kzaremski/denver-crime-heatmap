'''
CS 3120 Machine Learning Term Project
Denver Crime Heatmap
Konstantin Zaremski
December 1, 2024
'''

import pyproj

# Configuration constants
UPPER_LEFT_CORNER = (39.78597, -105.08110) # 39.78597° N, 105.08110° W
LOWER_RIGHT_CORNER = (39.63074, -104.81826) # 39.63074° N, 104.81826° W
GRID_SIZE = 50 # Grid Square Size in Meters

# Define projections: WGS84 for lat/lon and UTM Zone 13N for Denver
lat_lon_proj = pyproj.CRS("EPSG:4326")  # WGS84 (Lat/Lon)
utm_proj = pyproj.CRS("EPSG:26913")     # UTM Zone 13N

# Create transformer to convert Lat/Lon to UTM
transformer_to_utm = pyproj.Transformer.from_crs(lat_lon_proj, utm_proj, always_xy=True)

# Convert Lat/Lon to UTM
def lat_lon_to_utm(lat, lon):
    return transformer_to_utm.transform(lon, lat)  # Order is lon, lat

# Create transformer to convert UTM to Lat/Lon
transformer_to_latlon = pyproj.Transformer.from_crs(utm_proj, lat_lon_proj, always_xy=True)

# Convert UTM to Lat/Lon
def utm_to_lat_lon(utm_x, utm_y):
    return transformer_to_latlon.transform(utm_x, utm_y)  # Order is utm_x, utm_y

# Lat/Lon to block coordinate
def lat_lon_to_block(lat, lon):
    x, y = lat_lon_to_utm(lat, lon)
    x = int(x // GRID_SIZE)
    y = int(y // GRID_SIZE)
    return x, y

# Block coordinates to Lat/Lon
def block_to_lat_lon(x, y, position='upper_left'):
    """
    Convert block coordinates to latitude and longitude for a specified position within the block.
    
    Parameters:
        x (int): Block x-coordinate.
        y (int): Block y-coordinate.
        position (str): The position within the block. Can be 'upper_left', 'center', 
                        'upper_right', 'lower_left', or 'lower_right'.
                        
    Returns:
        tuple: Latitude and longitude of the specified position within the block.
    """
    utm_x = x * GRID_SIZE
    utm_y = y * GRID_SIZE

    if position == 'upper_left':
        pass  # No adjustment needed
    elif position == 'center':
        utm_x += GRID_SIZE / 2
        utm_y += GRID_SIZE / 2
    elif position == 'upper_right':
        utm_x += GRID_SIZE
    elif position == 'lower_left':
        utm_y += GRID_SIZE
    elif position == 'lower_right':
        utm_x += GRID_SIZE
        utm_y += GRID_SIZE
    else:
        raise ValueError("Invalid position. Use 'upper_left', 'center', 'upper_right', 'lower_left', or 'lower_right'.")
    
    return utm_to_lat_lon(utm_x, utm_y)

class MapGrid:
    """
    Class to represent a grid map based on geographical bounds.
    """
    def __init__(self, upper_left_bound, lower_right_bound, grid_size=GRID_SIZE):
        self.upper_left_bound = upper_left_bound
        self.lower_right_bound = lower_right_bound
        self.grid_size = grid_size
        self._calculate_bounds()
        self.grid = self._generate_grid()

    def _calculate_bounds(self):
        """
        Internal method to calculate UTM bounds and block ranges.
        """
        upper_left_utm = lat_lon_to_utm(*self.upper_left_bound)
        lower_right_utm = lat_lon_to_utm(*self.lower_right_bound)

        self.x_start = int(upper_left_utm[0] // self.grid_size)
        self.x_end = int(lower_right_utm[0] // self.grid_size)
        self.y_start = int(lower_right_utm[1] // self.grid_size)
        self.y_end = int(upper_left_utm[1] // self.grid_size)

    def _generate_grid(self):
        """
        Internal method to generate the grid based on bounds.
        """
        grid = []
        for x in range(self.x_start, self.x_end + 1):
            for y in range(self.y_start, self.y_end + 1):
                center_lat_lon = block_to_lat_lon(x, y, position='center')
                upper_left_lat_lon = block_to_lat_lon(x, y, position='upper_left')
                grid.append({
                    'block': (x, y),
                    'center_lat_lon': center_lat_lon,
                    'upper_left_lat_lon': upper_left_lat_lon
                })
        return grid

    def get_block_upper_left(self, x, y):
        """
        Get the upper left Lat/Lon of a specific block.
        """
        return block_to_lat_lon(x, y, position='upper_left')

    def get_block_center(self, x, y):
        """
        Get the center Lat/Lon of a specific block.
        """
        return block_to_lat_lon(x, y, position='center')

    def get_block_bounds(self, x, y):
        """
        Get all corner Lat/Lon positions for a specific block.
        """
        return {
            'upper_left': self.get_block_upper_left(x, y),
            'upper_right': block_to_lat_lon(x, y, position='upper_right'),
            'lower_left': block_to_lat_lon(x, y, position='lower_left'),
            'lower_right': block_to_lat_lon(x, y, position='lower_right')
        }

    def get_grid(self):
        """
        Return the entire grid data.
        """
        return self.grid

    def get_grid_size(self):
        """
        Return the grid size.
        """
        return self.grid_size

    def get_grid_dimensions(self):
        """
        Calculate the dimensions of the grid (number of blocks in x and y directions).
        """
        x_width = self.x_end - self.x_start + 1
        y_height = self.y_end - self.y_start + 1
        return x_width, y_height

#block = (10, 20)
#print(f"Bounds of block {block}: {grid_map.get_block_bounds(*block)}")

if __name__ == '__main__':
    map_grid = MapGrid(UPPER_LEFT_CORNER, LOWER_RIGHT_CORNER)
    print(f"Generated grid: {map_grid.get_grid_dimensions()} for a total of {len(map_grid.get_grid())} grid cells.")
