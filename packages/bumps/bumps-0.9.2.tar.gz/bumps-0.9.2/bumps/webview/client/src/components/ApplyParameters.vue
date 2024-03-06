<script setup lang="ts">
import { ref, onMounted, shallowRef } from 'vue';
import { Modal } from 'bootstrap/dist/js/bootstrap.esm';
import type { AsyncSocket } from '../asyncSocket';
import type { parameter_info } from './ParameterView.vue';

type ParameterToImport = {
  name: string,
  value: number,
  masked?: boolean,
}

const props = defineProps<{
  socket: AsyncSocket,
  title: string,
  parameters_in: ParameterToImport[],
  parameters: parameter_info[],
}>();

const dialog = ref<HTMLDivElement>();
const isOpen = ref(false);
const chosenFile = ref("");

let modal: Modal;
onMounted(() => {
  modal = new Modal(dialog.value, { backdrop: 'static', keyboard: false });
});

function close() {
  modal?.hide();
  isOpen.value = false;
}

async function open() {
  modal?.show();
  isOpen.value = true;
}

async function apply() {
  modal?.hide();
  console.log('applying!');
}

defineExpose({
  close,
  open
})
</script>

<template>
  <div ref="dialog" class="modal fade" id="applyParametersModal" tabindex="-1" aria-labelledby="applyParametersLabel"
    :aria-hidden="isOpen">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="applyParametersLabel">{{title}}</h5>
          <button type="button" class="btn-close" @click="close" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="container border-bottom">
            <h3>Parameters:</h3>
            <div class="row row-cols-3" v-for="param in parameters_in" :key="param.name">
              <div class="col overflow-hidden">{{param.name}}</div>
              <div class="col overflow-hidden">...model parameter</div>
            </div>
          </div>
          <!-- <div class="container border-bottom" v-if="show_files">
            <h3>Files:</h3>
            <div class="row row-cols-3">
              <div class="btn col overflow-hidden border" :class="{'btn-warning': filename == chosenFile}"
                v-for="filename in filelist" :key="filename + chosenFile" @click="chosenFile = filename" :title="filename"
                @dblclick="chosenFile=filename;chooseFile()">
                {{filename}}
              </div>
            </div>
          </div> -->
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="close">Cancel</button>
            <button type="button" class="btn btn-primary" @click="apply">Apply</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.active {
  background-color: light
}
</style>