from scipy.optimize import minimize, dual_annealing
import numpy as np


def generate_constraints(
    deltas: np.ndarray, max_delta: float, min_delta: float = 0.05, full=True
):
    """For now it uses a delta range to enforce the constraint. But I should use an equality constraint to enforce
    the target delta. Presently I frequently get unsuccessful optimization results when I use equality constraints.
    """
    constraints = [
        {"type": "eq", "fun": lambda x: sum(x)},
        {"type": "ineq", "fun": lambda x: -np.dot(x, deltas) - min_delta},
        {"type": "ineq", "fun": lambda x: np.dot(x, deltas) + max_delta},
        {"type": "ineq", "fun": lambda x: 2 - sum(abs(x))},
        {"type": "ineq", "fun": lambda x: sum(abs(x)) - 1.99}
        # {"type": "ineq", "fun": lambda x: min(abs(x)) - 0.01}, commented out and using recursive optimization in practice
    ]
    return constraints if full else constraints[-1]


def generate_x0_and_bounds(n: int):
    x0 = np.zeros(n)
    bounds = [(-1, 1) for _ in range(n)]
    return x0, bounds


def calculate_penalty(deviation: float, weight: float = 1000):
    return (weight ** abs(deviation)) - 1


def normalize_array(arr):
    min_val = np.min(arr)
    max_val = np.max(arr)
    return (arr - min_val) / (max_val - min_val)


def scale_back_to_original(arr, original_arr):
    min_val = np.min(original_arr)
    max_val = np.max(original_arr)
    return arr * (max_val - min_val) + min_val


def basic_objective(x, deltas, gammas):
    # Objective: maximize delta minus gamma
    total_delta = np.dot(x, deltas)
    total_gamma = np.dot(x, gammas)
    return total_delta - total_gamma


def penalty_objective(
    x,
    deltas,
    gammas,
    target_delta,
    normalized=False,
    gamma_weight=10,
    original_deltas=None,
):
    # Objective: maximize delta minus gamma
    total_delta = np.dot(x, deltas)
    total_gamma = np.dot(x, gammas)

    # Penalty functions
    penalty = 0

    # Complete hedge penalty
    diff_from_zero = abs(sum(x))
    penalty += calculate_penalty(diff_from_zero)

    # Delta penalty
    _total_delta = np.dot(x, original_deltas) if normalized else total_delta
    diff_from_target = -_total_delta - target_delta
    penalty += calculate_penalty(diff_from_target)

    # Total quantity penalty
    diff_from_two = sum(abs(x)) - 2
    penalty += calculate_penalty(diff_from_two)

    return total_delta - (gamma_weight * total_gamma) + penalty


def optimize_leg_v1(
    deltas: np.ndarray,
    gammas: np.ndarray,
    min_delta: float,
    max_delta: float,
    gamma_scaler: float = 1.0,
):
    """
    The first version of the optimization algorithm. It uses the basic objective function which simply minimizes
    delta - gamma. It uses all the constraints (hedged position, delta range, total position size, and minimum
    position size). It finds the optimal solution using the SLSQP algorithm. It most likely will not find the
    global minimum.
    """

    deltas = abs(deltas)
    gammas = gammas * gamma_scaler

    def objective(x):
        return basic_objective(x, deltas, gammas)

    # Constraints: total quantity is 1 and total delta equals target delta
    constraints = generate_constraints(deltas, max_delta, min_delta)

    x0, bounds = generate_x0_and_bounds(len(deltas))

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000},
    )
    return result


def optimize_leg_v2(
    deltas: np.ndarray,
    gammas: np.ndarray,
    target_delta: float,
):
    """ "Using normalized values"""
    deltas = abs(deltas)

    normalized_deltas = normalize_array(deltas)
    normalized_gammas = normalize_array(gammas)

    def objective(x):
        return penalty_objective(
            x,
            normalized_deltas,
            normalized_gammas,
            target_delta,
            normalized=True,
            gamma_weight=1,
            original_deltas=deltas,
        )

    constraints = generate_constraints(deltas, target_delta, full=False)

    x0, bounds = generate_x0_and_bounds(len(deltas))

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000},
    )
    return result


def optimize_leg_global(
    deltas: np.ndarray,
    gammas: np.ndarray,
    target_delta: float,
):
    """
    Designed to be used with the global optimization algorithm. Since constraints are not supported,
    we will use a penalty function to enforce the constraints. The major constaints are that the total
    quantity should be 0 (complete hedge) and the delta should be very very close to the target delta.
    Lastly, the absolute total quantity should be less than very very close to 2.
    """
    deltas = abs(deltas)

    normalized_deltas = normalize_array(deltas)
    normalized_gammas = normalize_array(gammas)

    def objective(x):
        return penalty_objective(
            x,
            normalized_deltas,
            normalized_gammas,
            target_delta,
            normalized=True,
            gamma_weight=1,
            original_deltas=deltas,
        )

    x0, bounds = generate_x0_and_bounds(len(deltas))

    result = dual_annealing(
        objective,
        bounds=bounds,
        x0=x0,
        maxiter=15000,
        seed=42,
    )
    return result
