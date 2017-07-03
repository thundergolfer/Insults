from insults.nn_model.util import strip_html, LossHistory


class TestLossHistory():

    def setup_method(self, method):
        self.loss_history = LossHistory()

    def test_on_train_begin(self):
        self.loss_history.on_train_begin()

        assert [] == self.loss_history.losses
        assert [] == self.loss_history.accuracies

    def test_on_batch_end(self):
        test_logs = {
            'loss': [1, 2, 3, 4, 5],
            'acc': [1, 2, 3, 4, 5]
        }

        self.loss_history.on_train_begin()
        self.loss_history.on_batch_end(None, test_logs)

        assert test_logs['loss'] == self.loss_history.losses[0]
        assert test_logs['acc'] == self.loss_history.accuracies[0]

        test_logs_second_batch = {
            'loss': [5, 4, 3, 2, 1],
            'acc': [5, 4, 3, 2, 1]
        }

        self.loss_history.on_batch_end(None, test_logs_second_batch)

        assert test_logs_second_batch['loss'] == self.loss_history.losses[1]
        assert test_logs_second_batch['acc'] == self.loss_history.accuracies[1]


def test_strip_html():
    test = "<p>This is a basic test string<br/> with html</p>"

    assert "This is a basic test string with html" == strip_html(test)
