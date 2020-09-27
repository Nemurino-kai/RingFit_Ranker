<template>
  <div class="user container">
  <h1>いままでの運動記録</h1>
      <hr style="margin-top:0.5em;margin-bottom:1em;">
                <form class="form-group form-inline" @submit.prevent="submitUsername">
                        <label>ユーザ名&nbsp;</label>
                        <input type="text" placeholder="Input Username ..." v-model="user" name="user">
                        &nbsp;<router-link v-bind:to="'/user/' + user" class="btn btn-primary">集計する</router-link>
                </form>
  <div class="overflow-auto" v-if="exercise_data.length != 0">
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="user-exercise-table"
      align="center"
    ></b-pagination>
      <b-table striped hover caption-top
      id="user-exercise-table"
          :items="exercise_data"
          :fields="columns"
          :per-page="perPage"
          :current-page="currentPage"
          small
    ></b-table>
        <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="user-exercise-table"
      align="center"
    ></b-pagination>
    <p class="mt-3" style="text-align:center;">displaying <b>{{(currentPage-1)* 100 + 1}} - {{Math.min(currentPage* 100, exercise_data.length)}}</b> records in total <b>{{exercise_data.length}}</b></p>
  </div>

  </div>
</template>

<script>
export default {
  data () {
    return {
      user: '',
      exercise_data: [],
      perPage: 100,
      currentPage: 1,
      columns: [ {
        label: 'Rank',
        key: 'daily_rank',
        sortable: true
      },
      {
        label: 'kcal',
        key: 'kcal',
        sortable: true
      },
      {
        label: 'Date',
        key: 'tweeted_time',
        sortable: true
      }]
    }
  },
  methods: {
    submitUsername: function () {
      this.$router.push(
        {
          path: '/user/' + this.user
        }
      )
    },
    modifyAPIResponse: function (res) {
      var modifyResult = res['data']['user_exercise_data_list']
      modifyResult = modifyResult.map(function (value) {
        value['daily_rank'] = value['daily_rank'] + '位'
        // 曜日に合わせて列の色を変える
        if (value['weeknumber'] === '6') {
          value['_rowVariant'] = 'info'
        }
        if (value['weeknumber'] === '0') {
          value['_rowVariant'] = 'danger'
        }
        return value
      })
      return modifyResult
    },
    readAPI: function () {
      this.$store.commit('view/start')
      this.user = this.$route.params.Username
      this.$api.get('https://ringfit.work/api/user?user=' + this.$route.params.Username).then(res => {
        this.exercise_data = this.modifyAPIResponse(res)
        this.$store.commit('view/end')
      })
    }
  },
  created: function () {
    if (this.$route.params.Username != null) {
      this.readAPI()
    }
  },
  watch: {
    $route (to, from) {
      this.readAPI()
    }
  },
  computed: {
    rows () {
      return this.exercise_data.length
    }
  }
}
</script>
