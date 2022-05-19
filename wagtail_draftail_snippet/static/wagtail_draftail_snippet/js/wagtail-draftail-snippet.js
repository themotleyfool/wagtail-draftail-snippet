(() => {
  'use strict';

  const React = window.React;
  const Modifier = window.DraftJS.Modifier;
  const AtomicBlockUtils = window.DraftJS.AtomicBlockUtils;
  const RichUtils = window.DraftJS.RichUtils;
  const EditorState = window.DraftJS.EditorState;

  const TooltipEntity = window.draftail.TooltipEntity;

  const global = globalThis;
  const $ = global.jQuery;

  const MUTABILITY = {};
  MUTABILITY['SNIPPET'] = 'MUTABLE';
  MUTABILITY['SNIPPET-EMBED'] = 'IMMUTABLE';

  const getSnippetModelChooserConfig = (entityType) => {
    let url;
    let urlParams;

    if (entityType.type === 'SNIPPET') {
      return {
        url: global.chooserUrls.snippetLinkModelChooser,
        urlParams: {},
        onload: global.SNIPPET_MODEL_CHOOSER_MODAL_ONLOAD_HANDLERS,
      };
    }
    else if (entityType.type === 'SNIPPET-EMBED') {
      return {
        url: global.chooserUrls.snippetEmbedModelChooser,
        urlParams: {},
        onload: global.SNIPPET_MODEL_CHOOSER_MODAL_ONLOAD_HANDLERS,
      };
    }
    else {
      return {
        url: null,
        urlParams: {},
        onload: {},
      };
    }
  };

  const getSnippetModelObjectChooserConfig = () => {
    let url;
    let urlParams;

    return {
      url: global.chooserUrls.snippetChooser.concat(window.snippetModelMeta.appName, '/', window.snippetModelMeta.modelName, '/'),
      urlParams: {},
      onload: global.SNIPPET_CHOOSER_MODAL_ONLOAD_HANDLERS,
    };
  };

  const filterSnippetEntityData = (entityType, data) => {
    return {
      edit_link: data.edit_link,
      string: data.string,
      id: data.id,
      app_name: window.snippetModelMeta.appName,
      model_name: window.snippetModelMeta.modelName,
    };
  };

  /**
   * Interfaces with Wagtail's ModalWorkflow to open the chooser,
   * and create new content in Draft.js based on the data.
   */
  class SnippetModalWorkflowSource extends React.Component {
    constructor(props) {
      super(props);

      this.onChosen = this.onChosen.bind(this);
      this.onClose = this.onClose.bind(this);
      this.onModelChosen = this.onModelChosen.bind(this);
    }

    componentDidMount() {
      const { onClose, entityType, entity, editorState } = this.props;
      const { url, urlParams, onload } = getSnippetModelChooserConfig(entityType);

      $(document.body).on('hidden.bs.modal', this.onClose);

      // eslint-disable-next-line new-cap
      this.model_workflow = global.ModalWorkflow({
        url,
        urlParams,
        onload,
        responses: {
          snippetModelChosen: this.onModelChosen,
        },
        onError: () => {
          // eslint-disable-next-line no-alert
          window.alert(global.wagtailConfig.STRINGS.SERVER_ERROR);
          onClose();
        },
      });
    }

    componentWillUnmount() {
      this.model_workflow = null;
      this.workflow = null;

      $(document.body).off('hidden.bs.modal', this.onClose);
    }

    onModelChosen(snippetModelMeta) {
      window.snippetModelMeta = snippetModelMeta;
      const { url, urlParams, onload } = getSnippetModelObjectChooserConfig();

      this.model_workflow.close();

      // eslint-disable-next-line new-cap
      this.workflow = global.ModalWorkflow({
        url,
        urlParams,
        onload,
        responses: {
          snippetChosen: this.onChosen,
        },
        onError: () => {
          // eslint-disable-next-line no-alert
          window.alert(global.wagtailConfig.STRINGS.SERVER_ERROR);
          onClose();
        },
      });
    }

    onChosen(data) {
      const { editorState, entityType, onComplete } = this.props;
      const content = editorState.getCurrentContent();
      const selection = editorState.getSelection();

      const entityData = filterSnippetEntityData(entityType, data);
      const mutability = MUTABILITY[entityType.type];
      const contentWithEntity = content.createEntity(entityType.type, mutability, entityData);
      const entityKey = contentWithEntity.getLastCreatedEntityKey();

      let nextState;

      if (entityType.block) {
        // Only supports adding entities at the moment, not editing existing ones.
        // See https://github.com/springload/draftail/blob/cdc8988fe2e3ac32374317f535a5338ab97e8637/examples/sources/ImageSource.js#L44-L62.
        // See https://github.com/springload/draftail/blob/cdc8988fe2e3ac32374317f535a5338ab97e8637/examples/sources/EmbedSource.js#L64-L91
        nextState = AtomicBlockUtils.insertAtomicBlock(editorState, entityKey, ' ');
      } else {
        // Replace text if the chooser demands it, or if there is no selected text in the first place.
        const shouldReplaceText = data.prefer_this_title_as_link_text || selection.isCollapsed();

        if (shouldReplaceText) {
          // If there is a title attribute, use it. Otherwise we inject the URL.
          const newText = data.string;
          const newContent = Modifier.replaceText(content, selection, newText, null, entityKey);
          nextState = EditorState.push(editorState, newContent, 'insert-characters');
        } else {
          nextState = RichUtils.toggleLink(editorState, selection, entityKey);
        }
      }

      // IE11 crashes when rendering the new entity in contenteditable if the modal is still open.
      // Other browsers do not mind. This is probably a focus management problem.
      // From the user's perspective, this is all happening too fast to notice either way.
      if (this.workflow) {
        this.workflow.close();
      }

      onComplete(nextState);
    }

    onClose(e) {
      const { onClose } = this.props;
      e.preventDefault();

      onClose();
    }

    render() {
      return null;
    }
  }

  const SnippetLink = props => {
    const { entityKey, contentState } = props;
    const data = contentState.getEntity(entityKey).getData();

    let icon = React.createElement(window.wagtail.components.Icon, {name: 'snippet'});
    let label = data.string || '';

    return React.createElement(TooltipEntity, {
      entityKey: props.entityKey,
      children: props.children,
      onEdit: props.onEdit,
      onRemove: props.onRemove,
      icon: icon,
      label: label
    });
  };

  const SnippetEmbed = props => {
    const { entity, onRemoveEntity, entityKey } = props.blockProps;
    const data = entity.getData();

    let icon = React.createElement(window.wagtail.components.Icon, {name: 'snippet'});
    let label = data.string || '';

    return React.createElement("div", {
      class: "MediaBlock"
    }, icon, `${label}`);
  };

  window.draftail.registerPlugin({
    type: 'SNIPPET',
    source: SnippetModalWorkflowSource,
    decorator: SnippetLink,
  });

  window.draftail.registerPlugin({
    type: 'SNIPPET-EMBED',
    source: SnippetModalWorkflowSource,
    block: SnippetEmbed,
  });
})();
