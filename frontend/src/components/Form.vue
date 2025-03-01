<script>
import * as yup from "yup";
import { Form, Field, ErrorMessage } from "vee-validate";
import AppService from "@/services/app.service";

export default {
  data() {
    const FormSchema = yup.object().shape({
      myFile: yup
        .mixed()
        .required()
    });
    return {
      FormSchema,
      image: null,
      imageUrl: null,
      isPredict: false,
      isLoading: false,
      result: null,
    }
  },
  components: {
    Form,
    Field,
    ErrorMessage,
  },
  methods: {
    async predict() {
      this.isLoading = true;
      var formdata = new FormData();
      formdata.append('myFile', this.image, this.image.name);
      var res = await AppService.predict(formdata);
      this.isPredict = true;
      if (res) {
        this.result = res.trim();
        this.isLoading = false;
      }
      else
        this.$router.go();
    },

    getImage(e) {
      this.image = e.target.files[0]
      this.imageUrl = URL.createObjectURL(this.image)
    },

    onDrop(e) {
      this.image = e.dataTransfer.files[0]
      this.imageUrl = URL.createObjectURL(this.image)
    },

    erase() {
      this.$router.go()
    },
  },
}
</script>

<template>
  <div v-if="isLoading" style="position: fixed; text-align: center; align-content: center; width: 100%; height: 100%;">
    <h1 class="text-primary">Processing...</h1>
  </div>
  <div class="" :style="[!isLoading ? { 'max-width': '900px', 'margin': 'auto' } : { 'max-width': '900px', 'margin': 'auto', 'background-color': 'white', 'opacity': '0.1' }]">
    <div v-if="!this.isPredict" class="mt-5" style="background-image: linear-gradient(rgb(220,230,250), rgb(135,165,220));">
      <Form @submit="predict" :validation-schema="FormSchema">
        <div class="row text-center py-3">
          <h2 class="">Identify Traffic Density</h2>
        </div>
        <hr style="height: 0.6rem; background-color: rgb(255,255,255); border: none; opacity: 1;">
        <div class="row p-5">
          <div class="row p-4" style="background-color: white; border-radius: 5px;">
            <div class="row p-5">
              <label @dragover.prevent @drop.prevent="onDrop" for="myFile" class="text-center" style="border-style: dotted; min-height: 15rem; background-color: rgb(249,249,249); align-content: center">
                <Field v-if="image==null" @change="getImage" tabindex="-1" single name="myFile" type="file" accept="image/*" style="display: none;" id="myFile" />
                <Field v-if="image!=null" @change="getImage" :value="''" tabindex="-1" single name="myFile" type="file" accept="image/*" style="display: none;" id="myFile" />
                <img v-if="!image" class="" src="@/assets/upload_information_16316.png" alt="" style="max-width: 100px; max-width: 100px;">
                <div v-if="imageUrl" style="display: flex; justify-content: center; align-items: center;">
                  <img class="" :src="imageUrl" alt="" style="max-width: 100px; max-width: 100px; object-fit: contain">
                  <div class="ms-2">{{ this.image.name }}</div>
                </div>
              </label>
            </div>
            <div class="row text-center fs-6 text-primary">
              <div>Upload an image and AI will show the answer.</div>
            </div>
            <div class="row mt-3 justify-content-center">
              <button type="submit" class="btn btn-primary p-2" style="max-width: 8rem;">Predict</button>
            </div>
          </div>
        </div>
      </Form>
    </div>
    <div v-if="this.isPredict" class="mt-5" style="background-image: linear-gradient(rgb(220,230,250), rgb(135,165,220));">
      <div class="row text-center py-3">
        <h2 class="">Identify Completed</h2>
      </div>
      <hr style="height: 0.6rem; background-color: rgb(255,255,255); border: none; opacity: 1;">
      <div class="row p-5 pb-3">
        <div class="row p-4 " style="background-color: white; border-radius: 5px;">
          <div class="row p-3 pt-0">
            <div class="row text-center pb-3">
              <h6 class="">The input image</h6>
            </div>
            <div style="display: flex; justify-content: center; align-items: center;">
              <img class="" :src="imageUrl" alt="" style="max-width: 500px; max-width: 500px; object-fit: contain">
            </div>
          </div>
        </div>
      </div>
      <div class="row p-3 mx-5 mb-3" style="background-color: white; border-radius: 5px;">
        <div v-if="result" class="row text-center">
          <div class="" style="display: flex; justify-content: center;">Traffic density result:&nbsp;
            <div v-if="result == 'Low'">{{ result }}</div>
            <div v-if="result == 'Medium'" class="text-primary">{{ result }}</div>
            <div v-if="result == 'High'" class="text-danger">{{ result }}</div>
          </div>
        </div>
      </div>
      <div class="row pb-3 justify-content-center">
        <button v-on:click="erase" class="btn btn-primary p-2" style="max-width: 8rem;">Return</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

a {
  text-decoration: none;
}
</style>