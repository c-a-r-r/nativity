<template>
<hr class="mt-4">
          <h3 class="mb-3">Price Information</h3>
        <div class="row g-3 mb-3">
        <div class="col-md-4">
              <label class="form-label">Price change</label>
              <div class="input-group">
                <span class="input-group-text" style="background: #c5ccc4;">$</span>
            <input v-model="form.itinerary_cost" class="form-control" />
          </div>
          </div>
          <div class="col-md-4">
            <label class="form-label">Commission Sales</label>
              <div class="input-group">
                <span class="input-group-text" style="background: #c5ccc4;">$</span>
            <input v-model="form.comision_usuario" class="form-control" />
          </div>
          </div>
          <div class="col-md-4">
            <label class="form-label">Fundraiser</label>
              <div class="input-group">
                <span class="input-group-text" style="background: #c5ccc4;">$</span>
            <input v-model="form.comision_leader" class="form-control" />
          </div>
          </div>
        </div>
        <div class="row g-3 mb-3">
          <div class="col-md-4">
            <label class="form-label" >Total Price</label>
                          <div class="input-group">
                <span class="input-group-text" style="background: #c5ccc4;">$</span>
            <input v-model="form.total_cost" class="form-control" readonly/>
          </div>
          </div>
          <div class="col-md-4">
            <label class="form-label">Land Only Price</label>
              <div class="input-group">
                <span class="input-group-text" style="background: #c5ccc4;">$</span>
            <input v-model="form.total_cost_land_only" class="form-control" />
          </div>
          </div>
        <div class="col-md-4">
          <label class="form-label">Display Commission Sales and Fundraiser</label>
          <select v-model="form.display_commission_fundraiser" class="form-select">
            <option value="NO">NO</option>
            <option value="YES">YES</option>
          </select>
        </div>
        </div>               
        <div class="row g-3 mb-3">
          <div class="col-md-4">
            <label class="form-label">Coordinator Name</label>
            <input v-model="form.coordinator_name" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Coordinator Phone</label>
            <input v-model="form.coordinator_phone" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Coordinator Email</label>
            <input v-model="form.coordinator_email" class="form-control" />
          </div>
        </div>        
        <div class="row g-3 mb-3">
         <div class="col-md-4">
            <label class="form-label">Language of Quote</label>
            <select v-model="form.language" class="form-select">
              <option value="">-- Select Language --</option>
              <option value="ENGLISH">ENGLISH</option>
              <option value="SPANISH">SPANISH</option>
              <option value="BILINGUAL">BILINGUAL</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Single Room Supplement</label>
            <input v-model="form.single_room_price" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Minimum Deposit</label>
              <div class="input-group">
              <span class="input-group-text" style="background: #c5ccc4;">$</span>          
            <input v-model="form.minimum_deposit" class="form-control" />
          </div>
          </div>
        </div>

          <div class="row g-3 mb-4">
            <div class="col-md-4">
              <label class="form-label">One Travels Free for each</label>
              <select v-model="form.free_each" class="form-select">
                <option value="0">NO FREE Travel</option>
                <option value="20">20</option>
                <option value="15">15</option>
                <option value="10">10</option>
                <option value="9">9</option>
                <option value="8">8</option>
                <option value="7">7</option>
                <option value="6">6</option>
                <option value="5">5</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Price change</label>
              <div class="input-group">
                <span class="input-group-text" id="basic-addon1" style="background: #c5ccc4;">$</span>
                <input
                  v-model="form.free_each_cost"
                  type="text"
                  class="form-control"
                  placeholder="0.00"
                  :readonly="form.free_each == 0 || form.free_each == 10"
                  aria-describedby="basic-addon1"
                />
              </div>
            </div>
          </div>

          <div class="row g-3 mb-4">
            <div class="col-md-4">
              <label class="form-label">Lunch and Tip Conditions</label>
              <select v-model="form.lunch_and_tip_includes" class="form-select">
                <option value="0">Does NOT Include Lunch and Tips</option>
                <option value="1">Includes Lunch</option>
                <option value="2">Includes Tips</option>
                <option value="3">Includes Lunch and Tips</option>
              </select>
            </div>
          </div>
          <div class="row g-3 mb-3">
            <div class="col-12 col-md-4">
              <label class="form-label">Lunch Included</label>
              <select v-model="form.lunch_included" class="form-select" :disabled="form.lunch_and_tip_includes == 0 || form.lunch_and_tip_includes == 2">
                <option value="NO">NO</option>
                <option value="YES">YES</option>
              </select>
            </div>
            <div class="col-12 col-md-3">
              <label class="form-label">Lunch cost $</label>
              <div class="input-group">
                <span class="input-group-text" style="background: #c5ccc4;">$</span>
              <input v-model="form.lunch_cost" class="form-control" :readonly="form.lunch_and_tip_includes == 0 || form.lunch_and_tip_includes == 2" />
            </div>
            </div>         
          </div>
          <div class="row g-3 mb-3">
            <div class="col-12 col-md-4">
              <label class="form-label">Tip Included</label>
              <select v-model="form.tip_included" class="form-select" :disabled="form.lunch_and_tip_includes == 0 || form.lunch_and_tip_includes == 1">
                <option value="NO">NO</option>
                <option value="YES">YES</option>
              </select>
            </div>
            <div class="col-12 col-md-3">
              <label class="form-label">Tips Cost $</label>
              <div class="input-group">
                <span class="input-group-text" style="background: #c5ccc4;">$</span>
              <input v-model="form.tips_cost" class="form-control" :readonly="form.lunch_and_tip_includes == 0 || form.lunch_and_tip_includes == 1" />
            </div>
            </div>
          </div>
</template>

<script setup>
const form    = defineModel()
const options = [0, 20, 15, 10, 9, 8, 7, 6, 5]

const FormInput = {
  props: { label:String, modelValue:[String,Number], readonly:Boolean },
  emits: ['update:modelValue'],
  template: `
    <div class="col-md-4">
      <label class="form-label">{{ label }}</label>
      <input :value="modelValue" class="form-control"
             :readonly="readonly"
             @input="$emit('update:modelValue', $event.target.value)">
    </div>`
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

* {
  font-size: 14px;
  font-weight: 400;
  font-family: 'Roboto', "Montserrat", sans-serif;
}

h3 {
  font-size: 25px;
  font-weight: 500;
  font-family: 'Roboto', "Montserrat", sans-serif;
}

</style>