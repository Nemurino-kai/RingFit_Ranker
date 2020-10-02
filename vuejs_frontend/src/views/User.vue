<template>
  <div class="user container">
  <h1>いままでの運動記録</h1>
      <hr style="margin-top:0.5em;margin-bottom:1em;">
                <form class="form-group form-inline" @submit.prevent="submitUsername">
                        <label>ユーザ名&nbsp;</label>
                        <input type="text" placeholder="Input Username ..." :value="userRank.user" name="user" ref="user">
                        &nbsp;<button type="submit" class="btn btn-primary">集計する</button>
                </form>
      <p class="mt-3" v-if='userRank.errored'>データを読み込めませんでした。ページを更新し直すか、時間をおいて再びアクセスしてください。</p>
  <div class="overflow-auto" v-if="rows != 0">
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="user-exercise-table"
      align="center"
    ></b-pagination>
      <b-table striped hover caption-top
      id="user-exercise-table"
          :items="userRank.exercise_data"
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
      @page-click="goTop"
    ></b-pagination>
    <p class="mt-3" style="text-align:center;">displaying <b>{{(currentPage-1)* 100 + 1}} - {{Math.min(currentPage* 100, rows)}}</b> records in total <b>{{rows}}</b></p>
  </div>

  </div>
</template>

<script>
import Chart from '@/components/Chart.vue'
import { mapState } from 'vuex'

export default {
  data () {
    return {
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
          path: '/user/' + this.$refs.user.value
        }
      )
    },
    goTop: function () {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    },
    checkParam: function () {
      if (this.$route.params.Username != null) {
        this.$store.dispatch('userRank/search', this.$route.params.Username)
      } else {
        this.$store.dispatch('userRank/reset')
      }
    }
  },
  created: function () {
    this.checkParam()
  },
  watch: {
    $route (to, from) {
      this.checkParam()
    }
  },
  computed: {
    ...mapState(['userRank']),
    rows () {
      return this.$store.state.userRank.exercise_data.length
    }
  }
}
</script>
