SNIPPET_MODEL_CHOOSER_MODAL_ONLOAD_HANDLERS = {
  'choose': function(modal, jsonData) {
    function getSelectedModelMeta(context) {
      $('a.snippet-model-choice', modal.body).on('click', function(event) {
        event.preventDefault();
        let modelMeta = {'appName': this.dataset.appName, 'modelName': this.dataset.modelName};
        modal.respond('snippetModelChosen', modelMeta);
        modal.close();
        $(".modal-backdrop").remove();
      });
    }

    getSelectedModelMeta(modal.body);
  },
};
