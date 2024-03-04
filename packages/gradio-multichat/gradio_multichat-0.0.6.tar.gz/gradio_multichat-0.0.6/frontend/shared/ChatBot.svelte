<script lang="ts">
  import { copy } from "@gradio/utils";
  import { dequal } from "dequal/lite";
  import { beforeUpdate, afterUpdate, createEventDispatcher } from "svelte";
  import { Audio } from "@gradio/audio/shared";
  import { Image } from "@gradio/image/shared";
  import { Video } from "@gradio/video/shared";
  import type { SelectData, LikeData } from "@gradio/utils";
  import { MarkdownCode as Markdown } from "@gradio/markdown";
  import { get_fetchable_url_or_file, type FileData } from "@gradio/client";
  import Copy from "./Copy.svelte";
  import LikeDislike from "./LikeDislike.svelte";
  import Pending from "./Pending.svelte";

  export let value: {
    role: string;
    position: "user" | "bot";
    avatar: string | null;
    message: string | { file: FileData; alt_text: string | null } | null;
    style: string | null;
  }[] = [];

  let old_value:
    | {
        role: string;
        position: "user" | "bot";
        avatar: string | null;
        message: string | { file: FileData; alt_text: string | null } | null;
        style: string | null;
      }[]
    | null = null;

  export let latex_delimiters: {
    left: string;
    right: string;
    display: boolean;
  }[];

  export let display_name = true;
  export let pending_message = false;
  export let selectable = false;
  export let likeable = false;
  export let rtl = false;
  export let show_copy_button = false;
  export let sanitize_html = true;
  export let bubble_full_width = true;
  export let render_markdown = true;
  export let line_breaks = true;
  export let root: string;
  export let proxy_url: null | string;
  export let layout: "bubble" | "panel" = "bubble";
  export let autoscroll: boolean = true;
  let div: HTMLDivElement;
  

  $: adjust_text_size = () => {
    let style = getComputedStyle(document.body);
    let body_text_size = style.getPropertyValue("--body-text-size");
    let updated_text_size: Number;

    switch (body_text_size) {
      case "13px":
        updated_text_size = 14;
        break;
      case "14px":
        updated_text_size = 16;
        break;
      case "16px":
        updated_text_size = 20;
        break;
      default:
        updated_text_size = 14;
        break;
    }

    document.body.style.setProperty(
      "--chatbot-body-text-size",
      updated_text_size + "px"
    );
  };

  $: adjust_text_size();

  const dispatch = createEventDispatcher<{
    change: undefined;
    select: SelectData;
    like: LikeData;
  }>();

  beforeUpdate(() => {
    autoscroll =
      div && div.offsetHeight + div.scrollTop > div.scrollHeight - 200;
  });

  const scroll = (): void => {
    if (autoscroll) {
      div.scrollTo(0, div.scrollHeight);
    }
  };
  afterUpdate(() => {
    if (autoscroll) {
      scroll();
      div.querySelectorAll("img").forEach((n) => {
        n.addEventListener("load", () => {
          scroll();
        });
      });
    }
  });

  $: {
    if (!dequal(value, old_value)) {
      old_value = value;
      dispatch("change");
    }
  }

  function handle_select(
    i: number,
    message: string | { file: FileData; alt_text: string | null } | null
  ): void {
    dispatch("select", {
      index: i,
      value: message,
    });
  }

  function handle_like(
    i: number,
    message: string | { file: FileData; alt_text: string | null } | null,
    selected: string | null
  ): void {
    dispatch("like", {
      index: i,
      value: message,
      liked: selected === "like",
    });
  }
</script>

<div
  class={layout === "bubble" ? "bubble-wrap" : "panel-wrap"}
  bind:this={div}
  role="log"
  aria-label="chatbot conversation"
  aria-live="polite"
>
  <div class="message-wrap" class:bubble-gap={layout === "bubble"} use:copy>
    {#if value !== null}
      {#each value as contents, i}
        {#if contents.message !== null}
          <div
            class="message-row {layout} {layout === 'panel'
              ? contents.style
              : ''}"
            class:user-row={contents.position === "user" &&
              (contents.style === null || layout === "bubble")}
            class:bot-row={contents.position === "bot" &&
              (contents.style === null || layout === "bubble")
              }
          >
            <div class="avatar-container">
              {#if contents.avatar !== null}
                <Image
                  class="avatar-image, topmargin"
                  src={get_fetchable_url_or_file(
                    contents.avatar,
                    root,
                    proxy_url
                  )}
                  alt="{contents.role} avatar"
                />
              {/if}
              {#if display_name}
                <div class="avatar-label">
                  {contents.role}
                </div>
              {/if}
            </div>
            <div
              class="message {contents.position === null
                ? 'unset'
                : contents.position} {contents.style}"
              class:message-fit={layout === "bubble" && !bubble_full_width}
              class:panel-full-width={layout === "panel"}
              class:message-bubble-border={layout === "bubble"}
              class:message-markdown-disabled={!render_markdown}
              style:text-align={rtl && contents.position === "user"
                ? "left"
                : "right"}
            >
              <button
                data-testid={contents.position === "user" ? "user" : "bot"}
                class:latest={i === value.length - 1}
                class:message-markdown-disabled={!render_markdown}
                style:user-select="text"
                class:selectable
                style:text-align={rtl ? "right" : "left"}
                on:click={() => handle_select(i, contents.message)}
                on:keydown={(e) => {
                  if (e.key === "Enter") {
                    handle_select(i, contents.message);
                  }
                }}
                dir={rtl ? "rtl" : "ltr"}
                aria-label={contents.role +
                  "'s message: " +
                  (typeof contents.message === "string"
                    ? contents.message
                    : `a file of type ${contents.message.file?.mime_type}, ${contents.message.file?.alt_text ?? contents.message.file?.orig_name ?? ""}`)}
              >
                {#if typeof contents.message === "string"}
                  <Markdown
                    message={contents.message}
                    {latex_delimiters}
                    {sanitize_html}
                    {render_markdown}
                    {line_breaks}
                    on:load={scroll}
                  />
                {:else if contents.message !== null && contents.message.file?.mime_type?.includes("audio")}
                  <Audio
                    data-testid="chatbot-audio"
                    controls
                    preload="metadata"
                    src={contents.message.file?.url}
                    title={contents.message.alt_text}
                    on:play
                    on:pause
                    on:ended
                  />
                {:else if contents.message !== null && contents.message.file?.mime_type?.includes("video")}
                  <Video
                    data-testid="chatbot-video"
                    controls
                    src={contents.message.file?.url}
                    title={contents.message.alt_text}
                    preload="auto"
                    on:play
                    on:pause
                    on:ended
                  >
                    <track kind="captions" />
                  </Video>
                {:else if contents.message !== null && contents.message.file?.mime_type?.includes("image")}
                  <Image
                    data-testid="chatbot-image"
                    src={contents.message.file?.url}
                    alt={contents.message.alt_text}
                  />
                {:else if contents.message !== null && contents.message.file?.url !== null}
                  <a
                    data-testid="chatbot-file"
                    href={contents.message.file?.url}
                    target="_blank"
                    download={contents.message.file?.orig_name ||
                      contents.message.file?.path}
                  >
                    {contents.message.file?.orig_name ||
                      contents.message.file?.path}
                  </a>
                {/if}
                {#if (likeable && contents.position !== "user") || (show_copy_button && contents.message && typeof contents.message === "string")}
                  <div class="message-buttons">
                    {#if likeable && contents.position !== "user"}
                      <LikeDislike
                        handle_action={(selected) =>
                          handle_like(i, contents.message, selected)}
                      />
                    {/if}
                    {#if show_copy_button && contents.message && typeof contents.message === "string"}
                      <Copy value={contents.message} />
                    {/if}
                  </div>
                {/if}
              </button>
            </div>
          </div>
        {/if}
      {/each}
      {#if pending_message}
        <Pending {layout} />
      {/if}
    {/if}
  </div>
</div>

<style>
  .message {
    position: relative;
    display: flex;
    flex-direction: column;
    align-self: flex-end;

    width: calc(100% - var(--spacing-xxl));
    color: var(--body-text-color);
    font-size: var(--chatbot-body-text-size);
    background: var(--background-fill-secondary);
    overflow-wrap: break-word;
    overflow-x: hidden;
    padding-right: calc(var(--spacing-xxl) + var(--spacing-md));
    padding: calc(var(--spacing-xxl) + var(--spacing-sm));
  }
  .message-wrap {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .bubble-gap {
    gap: calc(var(--spacing-xxl) + var(--spacing-lg));
  }
  .message-bubble-border {
    border-width: 1px;
    border-radius: var(--radius-xxl);
  }
  .message-fit {
    width: fit-content !important;
  }
  .panel-full-width {
    padding: calc(var(--spacing-xxl) * 2);
    width: 100%;
  }
  .message-markdown-disabled {
    white-space: pre-line;
  }

  @media (max-width: 480px) {
    .panel-full-width {
      padding: calc(var(--spacing-xxl) * 2);
    }
  }

  .message-row {
    display: flex;
    flex-direction: row;
    position: relative;
  }

  .message-row.panel.user-row {
    background: var(--color-accent-soft);
  }

  .message-row.panel.bot-row {
    background: var(--background-fill-secondary);
  }

  .message-row:last-of-type {
    margin-bottom: var(--spacing-xxl);
  }

  .user-row.bubble {
    flex-direction: row;
    justify-content: flex-end;
  }
  .message-wrap .message :global(img) {
    margin: var(--size-2);
    max-height: 200px;
  }
  .message-wrap .message :global(a) {
    color: var(--color-text-link);
    text-decoration: underline;
  }

  .message-wrap .bot :global(table),
  .message-wrap .bot :global(tr),
  .message-wrap .bot :global(td),
  .message-wrap .bot :global(th) {
    border: 1px solid var(--border-color-primary);
  }

  .message-wrap .user :global(table),
  .message-wrap .user :global(tr),
  .message-wrap .user :global(td),
  .message-wrap .user :global(th) {
    border: 1px solid var(--border-color-accent);
  }

  /* Lists */
  .message-wrap :global(ol),
  .message-wrap :global(ul) {
    padding-inline-start: 2em;
  }

  /* KaTeX */
  .message-wrap :global(span.katex) {
    font-size: var(--text-lg);
    direction: ltr;
  }

  /* Copy button */
  .message-wrap :global(div[class*="code_wrap"] > button) {
    position: absolute;
    top: var(--spacing-md);
    right: var(--spacing-md);
    z-index: 1;
    cursor: pointer;
    border-bottom-left-radius: var(--radius-sm);
    padding: 5px;
    padding: var(--spacing-md);
    width: 25px;
    height: 25px;
  }

  .message-wrap :global(code > button > span) {
    position: absolute;
    top: var(--spacing-md);
    right: var(--spacing-md);
    width: 12px;
    height: 12px;
  }
  .message-wrap :global(.check) {
    position: absolute;
    top: 0;
    right: 0;
    opacity: 0;
    z-index: var(--layer-top);
    transition: opacity 0.2s;
    background: var(--background-fill-primary);
    padding: var(--size-1);
    width: 100%;
    height: 100%;
    color: var(--body-text-color);
  }

  .message-wrap :global(pre) {
    position: relative;
  }

  .message-wrap > .message-row.panel {
    border-bottom: rgb(139, 139, 139) solid 1px;
  }

  .user {
    align-self: flex-start;
    border-bottom-right-radius: 0;
    text-align: right;
    border-color: var(--border-color-accent-subdued);
    background-color: var(--color-accent-soft);
  }

  .unset,
  .bot {
    text-align: left;
    border-color: var(--border-color-primary);
    background: var(--background-fill-secondary);
  }

  .bot {
    border-bottom-left-radius: 0;
  }

  .bubble-wrap {
    padding: var(--block-padding);
    width: 100%;
    overflow-y: auto;
  }

  .panel-wrap {
    width: 100%;
    overflow-y: auto;
  }

  @media (max-width: 480px) {
    .user-row.bubble {
      align-self: flex-end;
    }

    .bot-row.bubble {
      align-self: flex-start;
    }
    .message {
      width: auto;
    }
  }

  .avatar-container {
    bottom: 12px;
    top: 25px;
    position: sticky;
    width: 64px;
    height: 64px;
    z-index: 2;
    place-content: center;
    flex-flow: wrap;
  }

  .avatar-label {
    text-align: center;
    font-size: var(--text-lg) !important;
    font-weight: 600 !important;
  }

  /* Keep the code-box's original colors */

  .bot-row.bubble > .avatar-container,
  .user-row.bubble > .avatar-container {
    margin: 16px 10px 0;
    place-self: end;
  }

  .user-row.bubble > .avatar-container {
    display: flex;
    order: 2;
    align-content: flex-end;
  }
  .bot-row.bubble > .avatar-container {
    display: flex;
    align-content: flex-end;
  }

  .panel > .avatar-container {
    display: flex;
    align-content: flex-end;
    margin: 48px 8px 12px;
  }

  .avatar-container :global(img) {
    width: 64px;
    height: 64px;
    object-fit: cover;
    border-radius: 50%;
  }

  .message-buttons {
    display: flex;
    position: relative;
    margin-top: 1rem;
    border-radius: var(--radius-sm);
    justify-content: flex-start;
    bottom: -0.75rem;
    flex-wrap: wrap;
    align-items: center;
  }

  .user-row.bubble .message-buttons {
    justify-content: flex-end;
  }

  .share-button {
    position: absolute;
    top: 4px;
    right: 6px;
  }

  .selectable {
    cursor: pointer;
  }

  @keyframes dot-flashing {
    0% {
      opacity: 0.8;
    }
    50% {
      opacity: 0.5;
    }
    100% {
      opacity: 0.8;
    }
  }
</style>
