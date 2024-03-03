export default {
  meta: {
    inMenu: true,
    titleKey: "tezor.menu_title",
    icon: "mdi-piggy-bank-outline",
    permission: "tezor.view_menu_rule",
  },
  children: [
    {
      path: "invoice/:token/print/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.printInvoice",
    },
    {
      path: "invoice/:token/pay",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.doPayment",
    },
    {
      path: "clients/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.clients",
      meta: {
        inMenu: true,
        titleKey: "tezor.clients.menu_title",
        icon: "mdi-domain",
        permission: "tezor.can_view_clients",
      },
    },
    {
      path: "client/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.createClient",
    },
    {
      path: "client/:pk/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.editClientByPk",
    },
    {
      path: "client/:pk/delete/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.deleteClientByPk",
    },
    {
      path: "client/:pk/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.clientByPk",
    },
    {
      path: "client/:pk/invoice_groups/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.createInvoiceGroup",
    },
    {
      path: "invoice_group/:pk/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.editInvoiceGroupByPk",
    },
    {
      path: "invoice_group/:pk/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.invoiceGroupByPk",
    },
    {
      path: "invoice_group/:pk/delete/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.deleteInvoiceGroupByPk",
    },
    {
      path: "invoices/my/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.personalInvoices",
      meta: {
        inMenu: true,
        titleKey: "tezor.personal_invoices.menu_title",
        icon: "mdi-receipt-outline",
      },
    },
    {
      path: "invoice/:slug/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.invoiceByToken",
    },
    {
      path: "invoice/:token/send/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "tezor.sendInvoiceByToken",
    },
  ],
};
