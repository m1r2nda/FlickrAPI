PhotosViewModel = function () {
    var self = this;

    self.photos = ko.observableArray([])

    self.remove = function () {
        self.photos.pop()
    }

    self.isEmpty = ko.computed(function () {
        return self.photos().length === 0;
    });
	
	
    self.refresh = function () {
		 $.ajax({
        type: "POST",        
        url: '/photos',   
		data:JSON.stringify($('#search_text').val()),
		contentType: "application/json; charset=utf-8",
		dataType: "json",     
        async: false,         
		}).done(function (photos) {
			self.photos(photos);            
        });
		
    }

    self.run = function () {
         self.refresh();
    };
}


$(document).ready(function () {
    viewModel = new PhotosViewModel();
    ko.applyBindings(viewModel);
    viewModel.run();
});