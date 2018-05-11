<template> 
<transition name="modal">
 <div class="modal" style="display: block">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <slot name="header"></slot>
      </div>
      
      <div class="modal-body">
        <slot name="body"></slot>
      </div>
      
      <div class="modal-footer">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</div>
</transition> 
</template>
