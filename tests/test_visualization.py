from optuna.distributions import UniformDistribution
from optuna.study import create_study
from optuna.trial import Trial  # NOQA
from optuna.visualization import _get_contour_plot
from optuna.visualization import _get_intermediate_plot
from optuna.visualization import _get_optimization_history_plot
from optuna.visualization import _get_parallel_coordinate_plot
from optuna.visualization import _get_slice_plot


def test_get_intermediate_plot():
    # type: () -> None

    # Test with no trial.
    study = create_study()
    figure = _get_intermediate_plot(study)
    assert len(figure.data) == 0

    def objective(trial, report_intermediate_values):
        # type: (Trial, bool) -> float

        if report_intermediate_values:
            trial.report(1.0, step=0)
            trial.report(2.0, step=1)
        return 0.0

    # Test with a trial with intermediate values.
    study = create_study()
    study.optimize(lambda t: objective(t, True), n_trials=1)
    figure = _get_intermediate_plot(study)
    assert len(figure.data) == 1
    assert figure.data[0].x == (0, 1)
    assert figure.data[0].y == (1.0, 2.0)

    # Test with trials, one of which contains no intermediate value.
    study = create_study()
    study.optimize(lambda t: objective(t, False), n_trials=1)
    figure = _get_intermediate_plot(study)
    assert len(figure.data) == 1
    assert len(figure.data[0].x) == 0
    assert len(figure.data[0].y) == 0

    # Ignore failed trials.
    def fail_objective(_):
        # type: (Trial) -> float

        raise ValueError

    study = create_study()
    study.optimize(fail_objective, n_trials=1)
    figure = _get_intermediate_plot(study)
    assert len(figure.data) == 0


def test_get_optimization_history_plot():
    # type: () -> None

    # Test with no trial.
    study = create_study()
    figure = _get_optimization_history_plot(study)
    assert len(figure.data) == 0

    def objective(trial):
        # type: (Trial) -> float

        if trial.number == 0:
            return 1.0
        elif trial.number == 1:
            return 2.0
        elif trial.number == 2:
            return 0.0
        return 0.0

    # Test with a trial.
    study = create_study()
    study.optimize(objective, n_trials=3)
    figure = _get_optimization_history_plot(study)
    assert len(figure.data) == 2
    assert figure.data[0].x == (0, 1, 2)
    assert figure.data[0].y == (1.0, 2.0, 0.0)
    assert figure.data[1].x == (0, 1, 2)
    assert figure.data[1].y == (1.0, 1.0, 0.0)

    # Ignore failed trials.
    def fail_objective(_):
        # type: (Trial) -> float

        raise ValueError

    study = create_study()
    study.optimize(fail_objective, n_trials=1)
    figure = _get_optimization_history_plot(study)
    assert len(figure.data) == 0


def test_get_contour_plot():
    # type: () -> None

    # Test with no trial.
    study = create_study()
    figure = _get_contour_plot(study)
    assert len(figure.data) == 0

    study._append_trial(
        value=0.0,
        params={
            'param_a': 1.0,
            'param_b': 2.0,
        },
        distributions={
            'param_a': UniformDistribution(0.0, 3.0),
            'param_b': UniformDistribution(0.0, 3.0),
        }
    )
    study._append_trial(
        value=2.0,
        params={
            'param_b': 0.0,
        },
        distributions={
            'param_b': UniformDistribution(0.0, 3.0),
        }
    )
    study._append_trial(
        value=1.0,
        params={
            'param_a': 2.5,
            'param_b': 1.0,
        },
        distributions={
            'param_a': UniformDistribution(0.0, 3.0),
            'param_b': UniformDistribution(0.0, 3.0),
        }
    )

    # Test with a trial
    figure = _get_contour_plot(study)
    assert figure.data[0]['x'] == (1.0, 2.5)
    assert figure.data[0]['y'] == (0.0, 1.0, 2.0)
    assert figure.data[1]['x'] == (1.0, 2.5)
    assert figure.data[1]['y'] == (2.0, 1.0)
    assert figure.layout['xaxis']['range'] == (1.0, 2.5)
    assert figure.layout['yaxis']['range'] == (0.0, 2.0)

    # Test with a trial to select parameter
    figure = _get_contour_plot(study, params=['param_a', 'param_b'])
    assert figure.data[0]['x'] == (1.0, 2.5)
    assert figure.data[0]['y'] == (0.0, 1.0, 2.0)
    assert figure.data[1]['x'] == (1.0, 2.5)
    assert figure.data[1]['y'] == (2.0, 1.0)
    assert figure.layout['xaxis']['range'] == (1.0, 2.5)
    assert figure.layout['yaxis']['range'] == (0.0, 2.0)

    # Ignore failed trials.
    def fail_objective(_):
        # type: (Trial) -> float

        raise ValueError

    study = create_study()
    study.optimize(fail_objective, n_trials=1)
    figure = _get_contour_plot(study)
    assert len(figure.data) == 0


def test_get_parallel_coordinate_plot():
    # type: () -> None

    # Test with no trial.
    study = create_study()
    figure = _get_parallel_coordinate_plot(study)
    assert len(figure.data) == 0

    study._append_trial(
        value=0.0,
        params={
            'param_a': 1.0,
            'param_b': 2.0,
        },
        distributions={
            'param_a': UniformDistribution(0.0, 3.0),
            'param_b': UniformDistribution(0.0, 3.0),
        }
    )
    study._append_trial(
        value=2.0,
        params={
            'param_b': 0.0,
        },
        distributions={
            'param_b': UniformDistribution(0.0, 3.0),
        }
    )
    study._append_trial(
        value=1.0,
        params={
            'param_a': 2.5,
            'param_b': 1.0,
        },
        distributions={
            'param_a': UniformDistribution(0.0, 3.0),
            'param_b': UniformDistribution(0.0, 3.0),
        }
    )

    # Test with a trial.
    figure = _get_parallel_coordinate_plot(study)
    assert len(figure.data[0]['dimensions']) == 3
    assert figure.data[0]['dimensions'][0]['label'] == 'Objective Value'
    assert figure.data[0]['dimensions'][0]['range'] == (0.0, 2.0)
    assert figure.data[0]['dimensions'][0]['values'] == (0.0, 2.0, 1.0)
    assert figure.data[0]['dimensions'][1]['label'] == 'param_a'
    assert figure.data[0]['dimensions'][1]['range'] == (1.0, 2.5)
    assert figure.data[0]['dimensions'][1]['values'] == (1.0, 2.5)
    assert figure.data[0]['dimensions'][2]['label'] == 'param_b'
    assert figure.data[0]['dimensions'][2]['range'] == (0.0, 2.0)
    assert figure.data[0]['dimensions'][2]['values'] == (2.0, 0.0, 1.0)

    # Test with a trial to select parameter.
    figure = _get_parallel_coordinate_plot(study, params=['param_a'])
    assert len(figure.data[0]['dimensions']) == 2
    assert figure.data[0]['dimensions'][0]['label'] == 'Objective Value'
    assert figure.data[0]['dimensions'][0]['range'] == (0.0, 2.0)
    assert figure.data[0]['dimensions'][0]['values'] == (0.0, 2.0, 1.0)
    assert figure.data[0]['dimensions'][1]['label'] == 'param_a'
    assert figure.data[0]['dimensions'][1]['range'] == (1.0, 2.5)
    assert figure.data[0]['dimensions'][1]['values'] == (1.0, 2.5)

    # Ignore failed trials.
    def fail_objective(_):
        # type: (Trial) -> float

        raise ValueError

    study = create_study()
    study.optimize(fail_objective, n_trials=1)
    figure = _get_parallel_coordinate_plot(study)
    assert len(figure.data) == 0


def test_get_slice_plot():
    # type: () -> None

    # Test with no trial.
    study = create_study()
    figure = _get_slice_plot(study)
    assert len(figure.data) == 0

    study._append_trial(
        value=0.0,
        params={
            'param_a': 1.0,
            'param_b': 2.0,
        },
        distributions={
            'param_a': UniformDistribution(0.0, 3.0),
            'param_b': UniformDistribution(0.0, 3.0),
        }
    )
    study._append_trial(
        value=2.0,
        params={
            'param_b': 0.0,
        },
        distributions={
            'param_b': UniformDistribution(0.0, 3.0),
        }
    )
    study._append_trial(
        value=1.0,
        params={
            'param_a': 2.5,
            'param_b': 1.0,
        },
        distributions={
            'param_a': UniformDistribution(0.0, 3.0),
            'param_b': UniformDistribution(0.0, 3.0),
        }
    )

    # Test with a trial.
    figure = _get_slice_plot(study)
    assert len(figure.data) == 2
    assert figure.data[0]['x'] == (1.0, 2.5)
    assert figure.data[0]['y'] == (0.0, 1.0)
    assert figure.data[1]['x'] == (2.0, 0.0, 1.0)
    assert figure.data[1]['y'] == (0.0, 2.0, 1.0)

    # Test with a trial to select parameter.
    figure = _get_slice_plot(study, params=['param_a'])
    assert len(figure.data) == 1
    assert figure.data[0]['x'] == (1.0, 2.5)
    assert figure.data[0]['y'] == (0.0, 1.0)

    # Ignore failed trials.
    def fail_objective(_):
        # type: (Trial) -> float

        raise ValueError

    study = create_study()
    study.optimize(fail_objective, n_trials=1)
    figure = _get_slice_plot(study)
    assert len(figure.data) == 0
