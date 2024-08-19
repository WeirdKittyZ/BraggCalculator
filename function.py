import numpy as np

# =============================================================================
# Cell V Calculation
# =============================================================================
def cell_V(lattice_params):
    # Unpack lattice parameters and convert angles to radians
    a, b, c, alpha, beta, gamma = lattice_params
    alpha_rad = np.radians(alpha)
    beta_rad = np.radians(beta)
    gamma_rad = np.radians(gamma)
    
    # Construct the matrix for volume calculation
    matrix = np.array([[a**2, a*b*np.cos(gamma_rad), a*c*np.cos(beta_rad)], 
                       [a*b*np.cos(gamma_rad), b**2, b*c*np.cos(alpha_rad)],
                       [a*c*np.cos(beta_rad), c*b*np.cos(alpha_rad), c**2]])
    
    # Calculate the volume of the unit cell
    determinant = np.linalg.det(matrix)
    V = np.sqrt(determinant)
    return V

# =============================================================================
# Lattice Vectors to Cartesian Coordinates Conversion
# =============================================================================
def lattice_vectors_to_cartesian(lattice_params):
    # Unpack lattice parameters and convert angles to radians
    a, b, c, alpha, beta, gamma = lattice_params
    alpha_rad = np.deg2rad(alpha)
    beta_rad = np.deg2rad(beta)
    gamma_rad = np.deg2rad(gamma)
    
    # Calculate Cartesian coordinates for each lattice vector
    a_cartesian = np.array([a, 0, 0])
    b_cartesian = np.array([b * np.cos(gamma_rad), b * np.sin(gamma_rad), 0])
    c_cartesian = np.array([c * np.cos(beta_rad), 
                            c * (np.cos(alpha_rad) - np.cos(beta_rad) * np.cos(gamma_rad)) / np.sin(gamma_rad),
                            c * np.sin(beta_rad)])
    return a_cartesian, b_cartesian, c_cartesian

# =============================================================================
# Reciprocal Lattice Parameters Calculation
# =============================================================================
def reciprocal_latt(lattice_params):
    # Convert lattice vectors to Cartesian coordinates and calculate the volume of the unit cell
    a_cartesian, b_cartesian, c_cartesian = lattice_vectors_to_cartesian(lattice_params)
    V = cell_V(lattice_params)
    
    # Calculate reciprocal lattice vectors
    a_star_cartesian = np.cross(b_cartesian, c_cartesian) / V
    b_star_cartesian = np.cross(c_cartesian, a_cartesian) / V
    c_star_cartesian = np.cross(a_cartesian, b_cartesian) / V
    
    # Calculate angles and norms for reciprocal lattice vectors
    alpha_star = angle_between_vectors(b_star_cartesian, c_star_cartesian)
    beta_star = angle_between_vectors(a_star_cartesian, c_star_cartesian)
    gamma_star = angle_between_vectors(a_star_cartesian, b_star_cartesian)
    
    a_star = np.linalg.norm(a_star_cartesian)
    b_star = np.linalg.norm(b_star_cartesian)
    c_star = np.linalg.norm(c_star_cartesian)
    
    # Return the reciprocal lattice parameters
    reciprocal_params = a_star, b_star, c_star, alpha_star, beta_star, gamma_star
    return reciprocal_params

# =============================================================================
# Angle Between Two Vectors Calculation
# =============================================================================
def angle_between_vectors(v1, v2):
    # Compute the cosine of the angle between two vectors
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    # Convert the angle to degrees
    angle_degrees = np.degrees(np.arccos(cos_theta))
    return angle_degrees

# =============================================================================
# Bragg Angle Calculation
# =============================================================================
def bragg_angle(hkl, lattice_params, wavelength):
    # Unpack lattice parameters and Miller indices
    a, b, c, alpha, beta, gamma = lattice_params
    h, k, l = hkl
    alpha_rad = np.radians(alpha)
    beta_rad = np.radians(beta)
    gamma_rad = np.radians(gamma)
    
    # Calculate the volume of the unit cell and the interplanar spacing
    V = np.sqrt(a**2 * b**2 * c**2 * 
        (1 - np.cos(alpha_rad) ** 2 - np.cos(beta_rad) ** 2 - np.cos(gamma_rad) ** 2
        + 2 * np.cos(alpha_rad) * np.cos(beta_rad) * np.cos(gamma_rad)))

    d_hkl = V / np.sqrt(h ** 2 * (b ** 2 * c ** 2 * np.sin(alpha_rad) ** 2) +
                        k ** 2 * (a ** 2 * c ** 2 * np.sin(beta_rad) ** 2) +
                        l ** 2 * (a ** 2 * b ** 2 * np.sin(gamma_rad) ** 2)
                        + 2 * h * k * a * b * c ** 2 * (np.cos(alpha_rad) * np.cos(beta_rad) - np.cos(gamma_rad))
                        + 2 * h * l * a * b ** 2 * c * (np.cos(alpha_rad) * np.cos(gamma_rad) - np.cos(beta_rad))
                        + 2 * k * l * a ** 2 * b * c * (np.cos(beta_rad) * np.cos(gamma_rad) - np.cos(alpha_rad))
                        )
    
    # Calculate the Bragg angle
    two_theta = 2*np.degrees(np.arcsin(wavelength / (2 * d_hkl)))
    return d_hkl, two_theta


# =============================================================================
# Energy to Wavelength Conversion
# =============================================================================
def ev_to_angstrom(ev):
    # Convert energy from eV to wavelength in Ångström
    return 12398.425 / ev