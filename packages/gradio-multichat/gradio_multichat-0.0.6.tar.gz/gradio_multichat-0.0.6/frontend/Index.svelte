<script context="module" lang="ts">
  export { default as BaseChatBot } from "./shared/ChatBot.svelte";
</script>

<script lang="ts">
  import type { Gradio, SelectData, LikeData } from "@gradio/utils";

  import ChatBot from "./shared/ChatBot.svelte";
  import { Block, BlockLabel } from "@gradio/atoms";
  import type { LoadingStatus } from "@gradio/statustracker";
  import { Chat } from "@gradio/icons";
  import type { FileData } from "@gradio/client";
  import { StatusTracker } from "@gradio/statustracker";

  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;
  export let scale: number | null = null;
  export let min_width: number | undefined = undefined;
  export let label: string;
  export let show_label = true;
  export let root: string;
  export let proxy_url: null | string;
  export let _selectable = false;
  export let likeable = false;
  export let rtl = false;
  export let show_copy_button = false;
  export let sanitize_html = true;
  export let bubble_full_width = true;
  export let layout: "bubble" | "panel" = "bubble";
  export let render_markdown = true;
  export let line_breaks = true;
  export let display_name = true;
  export let autoscroll:boolean = true;
  export let latex_delimiters: {
    left: string;
    right: string;
    display: boolean;
  }[];

  export let value: {
    role: string;
    position: "user" | "bot" | null;
    avatar: string | null;
    message: string | { file: FileData; alt_text: string | null } | null;
    style: string | null;
  }[] = [];

  let _value: {
    role: string;
    position: "user" | "bot" | null;
    avatar: string | null;
    message: string | { file: FileData; alt_text: string | null } | null;
    style: string | null;
  }[];

  export let gradio: Gradio<{
    change: typeof value;
    select: SelectData;
    share: ShareData;
    error: string;
    like: LikeData;
  }>;

  const redirect_src_url = (src: string): string =>
    src.replace('src="/file', `src="${root}file`);

  function normalize_messages(
    message: { file: FileData; alt_text: string | null } | null
  ): { file: FileData; alt_text: string | null } | null {
    if (message === null) {
      return message;
    }
    return {
      file: message?.file as FileData,
      alt_text: message?.alt_text,
    };
  }

  $: _value = value
    ? value.map((item) => ({
        role: item.role,
        position: item.position,
        avatar: item.avatar,
        style: item.style,
        message:
          typeof item.message === "string"
            ? redirect_src_url(item.message)
            : normalize_messages(item.message),
      }))
    : [];

  export let loading_status: LoadingStatus | undefined = undefined;
  export let height = 400;
</script>

<Block
  {elem_id}
  {elem_classes}
  {visible}
  padding={false}
  {scale}
  {min_width}
  {height}
  allow_overflow={false}
>
  {#if loading_status}
    <StatusTracker
      autoscroll={gradio.autoscroll}
      i18n={gradio.i18n}
      {...loading_status}
      show_progress={loading_status.show_progress === "hidden"
        ? "hidden"
        : "minimal"}
    />
  {/if}
  <div class="wrapper">
    {#if show_label}
      <BlockLabel
        {show_label}
        Icon={Chat}
        float={false}
        label={label || "Chatbot"}
      />
    {/if}
    <ChatBot
      selectable={_selectable}
      {likeable}
      value={_value}
      {latex_delimiters}
      {render_markdown}
      pending_message={loading_status?.status === "pending"}
      {rtl}
      {show_copy_button}
      on:change={() => gradio.dispatch("change", value)}
      on:select={(e) => gradio.dispatch("select", e.detail)}
      on:like={(e) => gradio.dispatch("like", e.detail)}
      on:share={(e) => gradio.dispatch("share", e.detail)}
      on:error={(e) => gradio.dispatch("error", e.detail)}
      {sanitize_html}
      {bubble_full_width}
      {line_breaks}
      {layout}
      {proxy_url}
      {root}
      {display_name}
      {autoscroll}
    />
  </div>
</Block>

<style>
  .wrapper {
    display: flex;
    position: relative;
    flex-direction: column;
    align-items: start;
    width: 100%;
    height: 100%;
  }
</style>
