import unittest
import numpy as np
from lorenz_phase_space.phase_diagrams import Visualizer

class TestVisualizer(unittest.TestCase):

    def setUp(self):
        # Updated setup to reflect class initialization changes
        self.x_axis = np.array([1, 2, 3])
        self.y_axis = np.array([4, 5, 6])
        self.marker_color = np.array([7, 8, 9])
        self.marker_size = np.array([10, 11, 12])
        # Initialize with new zoom and limit options
        self.lps = Visualizer(LPS_type='mixed', zoom=True, 
                                    x_limits=(1, 3), y_limits=(4, 6),
                                    color_limits=(7, 9), marker_limits=(10, 12))

    def test_initialization(self):
        # Test initialization with new parameters
        self.assertEqual(self.lps.LPS_type, 'mixed')
        self.assertTrue(self.lps.zoom)

    def test_calculate_marker_size(self):
        # Updated to test with zoom parameter
        sizes, intervals = Visualizer.calculate_marker_size(self.marker_size, zoom=True)
        self.assertTrue(len(sizes) > 0)
        self.assertTrue(len(intervals) > 0)

    def test_get_labels(self):
        labels = self.lps.get_labels()
        self.assertIsInstance(labels, dict)
        self.assertIn('x_label', labels)
        self.assertIn('y_label', labels)

    def test_plot_data(self):
        # Update test to reflect method changes
        try:
            self.lps.plot_data(self.x_axis, self.y_axis, self.marker_color, self.marker_size)
            self.assertTrue(True)  # Confirm plot_data ran without error
        except Exception as e:
            self.fail(f"plot_data method failed with an exception: {e}")

    def test_zoom_with_random_factors(self):
        # Updated test to reflect dynamic limit adjustments
        n = len(self.x_axis)
        random_factors = np.random.randint(1, 11, size=n)
        x_axis_rdm = self.x_axis * random_factors
        y_axis_rdm = self.y_axis * random_factors
        marker_color_rdm = self.marker_color * random_factors
        marker_size_rdm = self.marker_size * random_factors

        # Recreate plot with updated dynamic limits based on random factors
        self.lps = Visualizer(LPS_type='mixed', zoom=True, 
                                    x_limits=[np.min(x_axis_rdm), np.max(x_axis_rdm)],
                                    y_limits=[np.min(y_axis_rdm), np.max(y_axis_rdm)],
                                    color_limits=[np.min(marker_color_rdm), np.max(marker_color_rdm)],
                                    marker_limits=[np.min(marker_size_rdm), np.max(marker_size_rdm)])
        
        self.lps.plot_data(x_axis_rdm, y_axis_rdm, marker_color_rdm, marker_size_rdm)
        try:
            self.lps.plot_data(x_axis_rdm, y_axis_rdm, marker_color_rdm, marker_size_rdm)
            self.assertTrue(True)  # Confirm plot_data with zoom and random factors ran without error
        except Exception as e:
            self.fail(f"plot_data with zoom and random factors failed with an exception: {e}")

if __name__ == '__main__':
    unittest.main()
