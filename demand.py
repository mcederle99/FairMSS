from scipy.stats import skellam
import numpy as np
import random


# Function to generate daily demand for a station type
def generate_daily_demand(station_count, demand_params, time_slots):
    demand_vectors = np.zeros((station_count, 24), dtype=np.int64)
    for i in range(station_count):
        daily_demand = np.concatenate([skellam.rvs(*params, size=end - start)
                                       for params, (start, end) in zip(demand_params, time_slots)])
        demand_vectors[i] = daily_demand
    return demand_vectors


def generate_global_demand(node_list, num_days, demand_params, time_slots):
    all_days_demand_vectors = []

    for _ in range(num_days):
        daily_demand_vectors = generate_daily_demand(node_list[0], demand_params[0], time_slots)
        for i in range(1, len(node_list)):
            demand_vectors_i = generate_daily_demand(node_list[i], demand_params[i], time_slots)
            # Combine demand vectors for the day
            daily_demand_vectors = np.vstack([daily_demand_vectors, demand_vectors_i])

        # Ensure total global demand equals zero
        for hour in range(24):
            total_demand = np.sum(daily_demand_vectors[:, hour])
            while total_demand != 0:
                adjustment = -1 if total_demand > 0 else 1
                random_station_index = random.randint(0, daily_demand_vectors.shape[0] - 1)
                daily_demand_vectors[random_station_index, hour] += adjustment
                total_demand += adjustment
        all_days_demand_vectors.append(daily_demand_vectors)

    # Transform the list of lists while maintaining the structure
    transformed_demand_vectors = []

    for sublist_day in all_days_demand_vectors:
        transformed_sublist_day = []
        for sublist_hour in sublist_day:
            transformed_sublist_hour = []

            # Transform each entry into a list of +1s, -1s, or 0
            for entry in sublist_hour:
                entry_int = int(entry)
                if entry_int > 0:
                    transformed_entry = [1] * entry_int
                elif entry_int < 0:
                    transformed_entry = [-1] * abs(entry_int)
                else:
                    transformed_entry = [0]
                transformed_sublist_hour.append(transformed_entry)

            transformed_sublist_day.append(transformed_sublist_hour)
        transformed_demand_vectors.append(transformed_sublist_day)

    return all_days_demand_vectors, transformed_demand_vectors
