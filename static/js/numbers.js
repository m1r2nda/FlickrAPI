NumbersViewModel = function () {
    var self = this;

    self.numbers = ko.observableArray([])

    self.remove = function () {
        self.numbers.pop()
    }

    self.isEmpty = ko.computed(function () {
        return self.numbers().length === 0;
    });

    self.refresh = function () {
        $.getJSON('/numbers').done(function (numbers) {
            self.numbers(numbers)
        });
    }

    self.run = function () {
        self.refresh();
    };
}


$(document).ready(function () {
    viewModel = new NumbersViewModel();
    ko.applyBindings(viewModel);
    viewModel.run();
});