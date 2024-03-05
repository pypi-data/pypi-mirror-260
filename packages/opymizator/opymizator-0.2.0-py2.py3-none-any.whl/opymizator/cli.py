import argparse
import pathlib
import optuna
import yaml
import csv

optuna.logging.set_verbosity(optuna.logging.CRITICAL)

# TODO: Rich terminal support
# TODO: add plan_X_predictions on the CLI
# TODO: add README.md


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "trials",
        type=pathlib.Path,
        help="Path to csv file with header containing the parameters and the results on the last column.",
    )
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        default=None,
        help="Path to a config file explaining the different parameters.",
    )
    return parser.parse_args()


def convert_to_ints(list_of_strings):
    try:
        result = [int(s) if len(s) else None for s in list_of_strings]
    except ValueError:
        return False, list_of_strings
    else:
        return True, result
    

def convert_to_floats(list_of_strings):
    try:
        result = [float(s) if len(s) else None for s in list_of_strings]
    except ValueError:
        return False, list_of_strings
    else:
        return True, result


def cli():
    args = parse_args()
    
    # Open configs
    config = {}
    if args.config is not None:
        with open(args.config, "r") as file:
            config = yaml.safe_load(file)

    with open(args.trials, "r") as file:
        trials_csv = list(csv.reader(file))
        parameters_name, *trials_csv = trials_csv
        results = [float(trial[-1]) if len(trial[-1]) else None for trial in trials_csv]
        trials = {
            parameters_name[idx_param]: [
                trial[idx_param] for idx_trial, trial in enumerate(trials_csv)
            ]
            for idx_param in range(len(parameters_name) - 1)
        }

    # Define sampler
    if "sampler" in config and "function" in config["sampler"]:
        sampler_name = config["sampler"].pop("function")
        sampler = getattr(optuna.samplers, sampler_name)(**config["sampler"])
    else:
        print("Sampler name has not been specified. Using TPESampler as default.")
        sampler = optuna.samplers.TPESampler()

    study = optuna.create_study(sampler=sampler)

    # Define distributions
    distributions = {parameter_name: None for parameter_name in trials.keys()}
    for name, kwargs in config.get("parameters", dict()).items():
        parameter_type = kwargs.pop("type")
        if parameter_type == "str":
            optuna_distri = optuna.distributions.CategoricalDistribution(**kwargs)
        elif parameter_type == "int":
            optuna_distri = optuna.distributions.IntDistribution(**kwargs)
        elif parameter_type == "float":
            optuna_distri = optuna.distributions.FloatDistribution(**kwargs)
        distributions[name] = optuna_distri

    for name, distribution in distributions.items():
        values = trials[name]
        if isinstance(distribution, optuna.distributions.FloatDistribution):
            _, values = convert_to_floats(values)
            trials[name] = values
        elif isinstance(distribution, optuna.distributions.IntDistribution):
            _, values = convert_to_ints(values)
            trials[name] = values
        elif isinstance(distribution, optuna.distributions.CategoricalDistribution):
            values = [s if len(s) else None for s in values]
            trials[name] = values
        else:
            print(
                f"Parameter {name} doesn't have a distribution. "
                "Guessing it from previous and future trials"
            )
            all_values_are_ints, values = convert_to_ints(values)
            if all_values_are_ints:
                trials[name] = values
                low = min(x for x in values if x is not None)
                high = max(x for x in values if x is not None)
                distributions[name] = optuna.distributions.IntDistribution(
                    low=low, high=high
                )
                print(
                    "Parameter's distribution was set to "
                    f"IntDistribution between {low} and {high}"
                )
                continue

            all_values_are_floats, values = convert_to_floats(values)
            if all_values_are_floats:
                trials[name] = values
                low = min(x for x in values if x is not None)
                high = max(x for x in values if x is not None)
                distributions[name] = optuna.distributions.FloatDistribution(
                    low=low, high=high
                )
                print(
                    "Parameter's distribution was set to "
                    f"FloatDistribution between {low} and {high}"
                )
            else:
                values = [s if len(s) else None for s in values]
                trials[name] = values
                choices = list(set(values) - set([None]))
                distributions[name] = optuna.distributions.CategoricalDistribution(
                    choices=choices
                )
                print(
                    "Parameter's distribution was set to "
                    f"CategoricalChoiceType with choices {choices}"
                )

    # add previous experiments
    for idx, result in enumerate(results):
        if result is not None:
            params = {key: values[idx] for key, values in trials.items()}
            trial = optuna.trial.create_trial(
                params=params,
                distributions=distributions,
                value=result,
            )
            study.add_trial(trial)


    # add constraints
    for idx, result in enumerate(results):
        if result is None:
            params = {
                key: values[idx]
                for key, values in trials.items()
                if values[idx] is not None
            }
            study.enqueue_trial(params)
            recommendation = study.ask(fixed_distributions=distributions).params
            trials_csv[idx] = [str(recommendation.get(name, '')) for name in parameters_name]


    with open(args.trials, "w") as file:
        writer_object = csv.writer(file)
        writer_object.writerow(parameters_name)
        writer_object.writerows(trials_csv)

    return
