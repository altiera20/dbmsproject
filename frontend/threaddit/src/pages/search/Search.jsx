import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useEffect } from "react";
import { Link, useSearchParams } from "react-router-dom";
import avatar from "../../assets/avatar.png";
import Loader from "../../components/Loader";
import Post from "../../components/Post";

const TABS = [
  { id: "all", label: "All" },
  { id: "post", label: "Posts" },
  { id: "comment", label: "Comments" },
  { id: "thread", label: "Communities" },
  { id: "user", label: "People" },
];

function Highlight({ html, fallback }) {
  if (html) {
    return <span dangerouslySetInnerHTML={{ __html: html }} />;
  }
  return <span>{fallback}</span>;
}

export function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get("q") || "";
  const type = searchParams.get("type") || "all";
  const { data, isFetching, isError, error } = useQuery({
    queryKey: ["search", query, type],
    queryFn: async ({ signal }) => {
      return await axios
        .get("/api/search", {
          params: { q: query, type, limit: 25 },
          signal,
        })
        .then((res) => res.data);
    },
    enabled: query.trim().length > 0,
    retry: false,
  });

  useEffect(() => {
    document.title = query ? `Search | ${query}` : "Search | Threaddit";
    return () => {
      document.title = "Threaddit";
    };
  }, [query]);

  function setType(nextType) {
    const next = new URLSearchParams(searchParams);
    next.set("type", nextType);
    setSearchParams(next, { replace: true });
  }

  const counts = data?.counts || {};
  const unavailable = isError && error?.response?.status === 503;

  return (
    <div className="flex flex-col flex-1 p-2 space-y-3 m-0.5 rounded-lg md:m-3 md:p-5 bg-theme-cultured md:bg-white">
      <header className="space-y-3">
        <h1 className="text-xl font-semibold md:text-2xl">
          {query ? (
            <>
              Results for <span className="text-theme-orange">&quot;{query}&quot;</span>
            </>
          ) : (
            "Search Threaddit"
          )}
        </h1>
        <p className="text-sm text-gray-600">
          Full-text search across posts, comments, communities, and people.
        </p>
        <div className="flex flex-wrap gap-2">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              type="button"
              className={`px-3 py-1.5 text-sm rounded-md ${
                type === tab.id ? "bg-theme-gray-blue font-semibold" : "hover:bg-theme-gray-blue"
              }`}
              onClick={() => setType(tab.id)}>
              {tab.label}
              {counts[tab.id] ? ` (${counts[tab.id]})` : ""}
            </button>
          ))}
        </div>
      </header>
      {!query.trim() && (
        <p className="p-5 bg-white rounded-xl border-2 border-theme-gray-blue">
          Type a query in the navbar search box to find posts, comments, communities, and users.
        </p>
      )}
      {isFetching && <Loader forPosts={true} />}
      {unavailable && (
        <p className="p-5 bg-white rounded-xl border-2 border-theme-gray-blue">
          Search is temporarily unavailable. Start Elasticsearch and reindex to use site search.
        </p>
      )}
      {data && !isFetching && data.results.length === 0 && query.trim() && (
        <p className="p-5 bg-white rounded-xl border-2 border-theme-gray-blue">
          No matches for &quot;{query}&quot;.
        </p>
      )}
      <ul className="flex flex-col space-y-3">
        {data?.results.map((item) => {
          if (item.type === "post" && item.post) {
            return <Post post={item.post} key={`post-${item.id}`} postIndex={0} />;
          }
          if (item.type === "comment") {
            return (
              <li key={`comment-${item.id}`} className="p-4 bg-white rounded-xl border-2 border-theme-gray-blue">
                <p className="text-xs text-gray-500">
                  Comment by{" "}
                  <Link className="text-blue-600 hover:underline" to={`/u/${item.comment.user_name}`}>
                    u/{item.comment.user_name}
                  </Link>{" "}
                  on{" "}
                  <Link className="font-medium hover:underline text-theme-orange" to={`/post/${item.comment.post_id}`}>
                    {item.comment.post_title || "a post"}
                  </Link>
                </p>
                <p className="mt-2 text-sm md:text-base">
                  <Highlight html={item.highlight} fallback={item.comment.content} />
                </p>
              </li>
            );
          }
          if (item.type === "thread") {
            const threadPath = `/${item.thread.name}`;
            return (
              <li key={`thread-${item.id}`}>
                <Link
                  to={threadPath}
                  className="flex items-center p-4 space-x-4 bg-white rounded-xl border-2 border-theme-gray-blue hover:drop-shadow-md">
                  {item.thread.logo && (
                    <img src={item.thread.logo} alt="" className="object-cover w-12 h-12 rounded-full" />
                  )}
                  <div>
                    <p className="font-semibold">{item.thread.name}</p>
                    <p className="text-sm text-gray-600">{item.thread.description}</p>
                    <p className="text-xs text-gray-500">{item.thread.subscriberCount} members</p>
                  </div>
                </Link>
              </li>
            );
          }
          if (item.type === "user") {
            return (
              <li key={`user-${item.id}`}>
                <Link
                  to={`/u/${item.user.username}`}
                  className="flex items-center p-4 space-x-4 bg-white rounded-xl border-2 border-theme-gray-blue hover:drop-shadow-md">
                  <img
                    src={item.user.avatar || avatar}
                    alt=""
                    className="object-cover w-12 h-12 rounded-full"
                  />
                  <div>
                    <p className="font-semibold">u/{item.user.username}</p>
                    {item.user.bio && <p className="text-sm text-gray-600">{item.user.bio}</p>}
                    <p className="text-xs text-gray-500">karma: {item.user.karma?.user_karma || 0}</p>
                  </div>
                </Link>
              </li>
            );
          }
          return null;
        })}
      </ul>
    </div>
  );
}

export default Search;
